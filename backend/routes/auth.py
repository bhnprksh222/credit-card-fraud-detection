"""
File Name   : auth.py
Author      : Bhanu Prakash Akepogu
Date        : 03/25/2025
Description : This script initiates the auth route, helps to signup and login
Version     : 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from logger import logger
from models.user import User
from schemas.auth import Token
from schemas.user import UserCreate, UserOut
from utils.auth import create_access_token, get_password_hash, verify_password

router = APIRouter()


@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate):
    try:
        existing_user = await User.get_or_none(email=user.email)
        if existing_user:
            raise HTTPException(status_code=409, detail="User already exists")
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
        raise HTTPException(status_code=500, detail="Signup failed")


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info("entered")
    user = await User.get_or_none(username=form_data.username)
    logger.info(f"user: {user}")
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    logger.info(f"token: {token}")
    return {"access_token": token, "token_type": "bearer"}
