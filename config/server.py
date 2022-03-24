from fastapi import FastAPI

from api import add_router
from config.settings import get_api_settings

settings = get_api_settings()


def create_app():
    app = FastAPI(**settings.fastapi_kwargs)
    add_router(app)

    return app
