from models.user import User
from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    password: str


UserOut = pydantic_model_creator(User, name="UserOut", exclude=("password_hash",))


class UserSearchResult(BaseModel):
    id: str
    username: str
    firstname: str
    lastname: str
    email: EmailStr
