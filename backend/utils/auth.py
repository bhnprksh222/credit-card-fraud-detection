from datetime import datetime, timedelta

from config import current_config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
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
    encoded_jwt = jwt.encode(
        to_encode, current_config.SECRET_KEY, algorithm=current_config.ALGORITHM
    )
    return encoded_jwt


# -----------------------------
# User Retrieval from Token
# -----------------------------


async def get_user_from_token(token: str):
    try:
        payload = jwt.decode(
            token, current_config.SECRET_KEY, algorithms=[current_config.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return await User.get_or_none(id=user_id)
    except JWTError:
        return None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, current_config.SECRET_KEY, algorithms=[current_config.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

        user = await User.get_or_none(id=user_id)
        if user is None:
            raise credentials_exception
            return user
