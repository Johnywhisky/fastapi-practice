from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from .exctions import UserNotFoundError, EmailUserExistsError
from .models import PrimaryKey
from .schemas import UserRegisterResponse, UserRead, UserRegister
from .services import get, get_by_email, create
from src.database.core import get_db


auth_router = APIRouter()
user_router = APIRouter()


@auth_router.post("/register", response_model=UserRegisterResponse)
def register_user(user_schema: UserRegister, db_session: Session = Depends(get_db)):
    user = get_by_email(db_session=db_session, email=user_schema.email)
    if user:
        raise EmailUserExistsError
    user = create(db_session=db_session, user_schema=user_schema)
    return user


@user_router.get("/{user_id}", response_model=UserRead)
def get_user(*, db_session: Session = Depends(get_db), user_id: PrimaryKey):
    """Get a user."""
    user = get(db_session=db_session, user_id=user_id)
    if not user:
        raise UserNotFoundError
    return user
