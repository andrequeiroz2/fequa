from pydantic import BaseModel
from typing import List


class UserSchema(BaseModel):
    username: str
    email: str


class UserListSchema(BaseModel):
    users: List[UserSchema]
    total: int


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str


class UserDB(BaseModel):
    username: str
    email: str
    password: str


class UserPassSchema(UserSchema):
    hashed_password: str


class UserTokenSchema(UserSchema):
    access_token: str
    token_type: str = "bearer"
