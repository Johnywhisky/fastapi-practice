from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.api import api_router


api = FastAPI(root_path="/api/v0/")

api.include_router(api_router)
api.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])

app = FastAPI()
app.mount(path="/api/v0", app=api)
