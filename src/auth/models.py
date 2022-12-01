"""Declare Database Auth Model
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict

import bcrypt
import jwt
from pydantic.types import conint
from sqlalchemy import Boolean, Column, Integer, LargeBinary, String

from src.config import JWT_ALG, JWT_AC_EXP, JWT_RE_EXP, JWT_SECRET
from src.database.core import Base, engine
from src.database.models import BaseModelMixin


PrimaryKey = conint(gt=0, lt=2147483647)


def hash_password(password: str) -> bytes:
    """Generates a hashed version of the provided password.
    :param password: The provided password
    :return: bytes"""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


async def generate_access_token(email: str, now: datetime) -> str:
    exp = (now + timedelta(days=JWT_AC_EXP)).timestamp()
    payload = {"exp": exp, "email": email, "type": "access"}
    res = jwt.encode(
        payload=payload, key=JWT_SECRET, algorithm=JWT_ALG, headers={"typ": "JWT", "alg": JWT_ALG}
    )
    print(type(res), res)
    return res


async def generate_refresh_token(now) -> str:
    exp = (now + timedelta(days=JWT_RE_EXP)).timestamp()
    payload = {"exp": exp, "type": "refresh"}
    return jwt.encode(
        payload=payload, key=JWT_SECRET, algorithm=JWT_ALG, headers={"typ": "JWT", "alg": JWT_ALG}
    )


async def generate_tokens(email: str) -> Dict[str, str]:
    now = datetime.utcnow()
    access_token, refresh_token = await asyncio.gather(
        *[generate_access_token(email, now), generate_refresh_token(now)]
    )
    print(access_token, refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token}


class User(Base, BaseModelMixin):
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(LargeBinary, nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, default=0, nullable=True)

    is_active = Column(Boolean, default=False, nullable=False)
    is_staff = Column(Boolean, default=False, nullable=False)

    @property
    def name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    @property
    def tokens(self) -> Dict[str, str]:
        tokens = asyncio.run(generate_tokens(self.email))
        print(tokens)
        return tokens

    class Config:
        orm_mode = True
        validate_assignment = True

    def check_password(self, password: bytes) -> bool:
        """Compare the provided password with hashed password
        :param password: provided password
        :return: True or False
        """
        return bcrypt.checkpw(password=password, hashed_password=self.password)


Base.metadata.create_all(bind=engine)
