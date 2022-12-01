from fastapi.exceptions import HTTPException
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from starlette import status

from .schemas import UserRegister
from src.exceptions import ExistsError


EmailUserExistsError = ValidationError(
    [ErrorWrapper(ExistsError(msg="A user with this email already exists."), loc="email")],
    model=UserRegister,
)

FORBIDDEN_USER_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=[{"msg": "..."}],
)

UserNotFoundError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=[{"msg": "A user with this id does not exist."}],
)
