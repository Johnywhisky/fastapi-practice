import time
from typing import Callable, List

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.routing import APIRoute
from pydantic import BaseModel

from src.auth.views import auth_router, user_router
from src.scraper.views import scraper_router


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: List[ErrorMessage] | None


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            return response

        return custom_route_handler


api_router = APIRouter(
    route_class=TimedRoute,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)


api_router.include_router(scraper_router, prefix="/scraper", tags=["scraper"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/user", tags=["user"])

# WARNING: Don't use this unless you want unauthenticated routes
authenticated_api_router = APIRouter()
