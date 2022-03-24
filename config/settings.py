from functools import lru_cache
from pydantic import (
    BaseSettings,
    PostgresDsn
)
from typing import Any, Dict


class APISettings(BaseSettings):
    title: str = "mealing_test"
    version: str = "0.1.0"
    PROJECT_ENV: str

    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    @property
    def get_db_url(self) -> PostgresDsn:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    docs_url: str = "/docs/"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json/"
    redoc_url: str = "/redoc/"


    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        fastapi_kwargs: Dict[str, Any] = {
            "debug": False if self.PROJECT_ENV == "production" else True,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }
        return fastapi_kwargs

    class Config:
        env_file = ".env"
        validate_assignment = True


@lru_cache()
def get_api_settings() -> APISettings:
    return APISettings()