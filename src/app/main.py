from fastapi import FastAPI

from app.apis.api_v1 import api_router

app = FastAPI(title="Base FastAPI with OAuth2 support")

app.include_router(api_router, prefix="/api/v1")
