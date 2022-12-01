import logging
from pathlib import Path
from typing import Dict
from urllib import parse

from pydantic import BaseModel
from starlette.config import Config
from starlette.datastructures import Secret


log = logging.getLogger(__name__)


class ConfigurationModel(BaseModel):
    pass


BASE_DIR = Path(__file__).resolve().parent.parent

config = Config(BASE_DIR / "env" / ".env")

TITLE = config("TITLE", default="fastapi_practice")
VERSION = config("VERSION", default="0.1.0")

# Database Config
DB_NAME = config("DB_NAME")
DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", default="5432")
DB_USER = config("DB_USER")
_DB_PASSWORD = config("DB_PASSWORD", cast=Secret)
_QUOTED_DB_PASSWORD = parse.quote(str(_DB_PASSWORD))

if all([DB_NAME, DB_HOST, DB_PORT, DB_USER, _QUOTED_DB_PASSWORD]):
    DB_URI = f"postgresql://{DB_USER}:{_QUOTED_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DB_URI = f"postgresql://johnywhisky:@localhost:5432/fastapi_practice"

docs_url = config("docs_url", default="/v1/docs/")
openapi_prefix = config("openapi_prefix", default="")
openapi_url = config("openapi_url", default="/openapi.json/")
redoc_url = config("redoc_url", default="/redoc/")

# OpenAPI Config
NAVER_CLIENT_CREDENTIAL = config("NAVER_CLIENT_CREDENTIAL", cast=Secret)
_NAVER_CLIENT_ID, _NAVER_CLIENT_SECRET = str(NAVER_CLIENT_CREDENTIAL).split(":")
NAVER_HEADERS: Dict[str, str] = {
    "X-Naver-Client-Id": _NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": _NAVER_CLIENT_SECRET,
}
KAKAO_CLIENT_ID = None
KAKAO_CLIENT_SECRET = None

# JWT Config
JWT_ALG = config("JWT_ALG", default="")
JWT_SECRET = config("JWT_SECRET", cast=Secret)
JWT_AC_EXP = 7
JWT_RE_EXP = 30
