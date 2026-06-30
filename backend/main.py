from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config.constants import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    API_V1_PREFIX,
)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
)

app.include_router(
    api_router,
    prefix=API_V1_PREFIX,
)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {APP_NAME}"
    }