import asyncio
from datetime import datetime, timedelta
from typing import Dict

import bcrypt
import jwt
from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session

from .models import User
from .schemas import UserRegister

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail=[{"msg": "Invalidate credentials"}]
)


def get(db_session: Session, user_id: int) -> User | None:
    """Returns a user based on the given user id."""
    if not db_session:
        raise
    if not isinstance(user_id, int):
        raise TypeError()
    return db_session.query(User).filter(User.id == user_id).one_or_none()


def get_by_email(db_session: Session, email: str) -> User | None:
    if not db_session:
        raise
    if not isinstance(email, str):
        raise TypeError()
    return db_session.query(User).filter(User.email == email).one_or_none()


def filter():
    ...


def create(*, db_session: Session, user_schema: UserRegister) -> User:
    password: bytes = bytes(user_schema.password, "utf-8")
    user = User(
        **user_schema.dict(exclude={"password"}),
        password=password,
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()
    db_session.commit()
    db_session.refresh(user)

    return user


def update():
    ...


def delete():
    ...
