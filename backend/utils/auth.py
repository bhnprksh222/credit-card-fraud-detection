from datetime import datetime, timedelta

from config import current_config
from fastapi import HTTPException, Request, status
from jose import JWTError, jwt
from models.user import User
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------
# Password Utilities
# -----------------------------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -----------------------------
# JWT Utilities
# -----------------------------
def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=60)
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, current_config.SECRET_KEY, algorithm=current_config.ALGORITHM
    )


# -----------------------------
# User Retrieval from Cookie Token
# -----------------------------
async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials missing",
        )

    try:
        payload = jwt.decode(
            token, current_config.SECRET_KEY, algorithms=[current_config.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token decode error",
        )

    user = await User.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
