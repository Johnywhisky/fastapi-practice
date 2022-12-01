"""Declare Auth Pydantic Model"""
from typing import Dict

from pydantic import Field, validator

from .models import hash_password
from src.database.schemas import MyBase


class UserBase(MyBase):
    age: int
    first_name: str
    last_name: str
    email: str


class UserLogin(UserBase):
    password: str

    @validator("password")
    def password_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string")
        return v


class UserRegister(UserLogin):
    password: str | None = Field(None, nullable=True)

    @validator("password", pre=True, always=True)
    def password_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string")
        return hash_password(v)


class UserRead(MyBase):
    age: int
    email: str
    is_active: bool
    name: str


class UserRegisterResponse(UserRead):
    tokens: Dict[str, str]
