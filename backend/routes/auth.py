"""
File Name   : auth.py
Author      : Bhanu Prakash Akepogu
Date        : 03/25/2025
Description : This script handles signup, email/password login, and Google OAuth with httpOnly JWT cookies.
Version     : 1.1.0
"""

import os

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from logger import logger
from models.user import User
from schemas.auth import Token
from schemas.user import UserCreate, UserOut
from utils.auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

router = APIRouter()
oauth = OAuth()

# Register Google OAuth
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# -------------------------------------------
# Email/Password Signup
# -------------------------------------------
@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate):
    try:
        existing_user = await User.get_or_none(email=user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )
        user_obj = await User.create(
            username=user.username,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            password_hash=get_password_hash(user.password),
        )
        return await UserOut.from_tortoise_orm(user_obj)
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Signup failed",
        )


# -------------------------------------------
# Email/Password Login - sets cookie
# -------------------------------------------
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(
        username=form_data.username
    ) or await User.get_or_none(email=form_data.username)

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token({"sub": str(user.id)})

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production (HTTPS only)
        samesite="lax",
        max_age=60 * 60 * 24,  # 1 day
    )
    return response


# -------------------------------------------
# Google OAuth - start redirect
# -------------------------------------------
@router.get("/google")
async def google_login(request: Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URL")
    return await oauth.google.authorize_redirect(request, redirect_uri)


# -------------------------------------------
# Google OAuth Callback - create user + set cookie
# -------------------------------------------
@router.get("/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)

    email = user_info["email"]
    username = user_info["name"].replace(" ", "_").lower()

    user = await User.get_or_none(email=email)
    if not user:
        user = await User.create(
            username=username,
            email=email,
            firstname=user_info.get("given_name", ""),
            lastname=user_info.get("family_name", ""),
            password_hash="oauth_google_user",
        )

    jwt_token = create_access_token(data={"sub": str(user.id)})

    redirect_url = os.getenv("FRONTEND_URL") + "/dashboard"
    response = RedirectResponse(url=redirect_url)
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24,
    )
    return response


@router.get("/me")
async def get_profile(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "firstname": user.firstname}


@router.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    return response
