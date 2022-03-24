from fastapi import FastAPI

from .health_check import base_router
from .user import user_router

routers = [base_router, user_router]

def add_router(app: FastAPI) -> None:
    [app.include_router(router) for router in routers]
