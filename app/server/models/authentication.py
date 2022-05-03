from typing import Optional

from bson import ObjectId
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None
    _id: Optional[ObjectId] = None
    username: Optional[str]
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    company_id: Optional[str] = None


class Token(BaseModel):
    access_token: Optional[str]
    token_type: Optional[str]


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(TokenData):
    password: Optional[str] = None


class UserRegistration(User):
    password1: Optional[str]
    password2: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "username": "john123",
                "email": "doe@gmail.com",
                "full_name": "John Doe",
                "password1": "*************",
                "password2": "*************",
                "company_id": "company_id",
            }
        }


class UserInDB(User):
    hashed_password: Optional[str] = None
