from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from env import CLIENT_DOMAIN, CORS_ORIGINS
from src.routers import (
    admin_router,
    tool_router

)

def create_api():
    api = FastAPI(title="Framed API", version="0.0.1", debug=True)
    include_routers(api)
    add_middleware(api)
    return api

def add_middleware(api: FastAPI):
    api.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def include_routers(api: FastAPI):
    api.include_router(admin_router)
    api.include_router(tool_router)
