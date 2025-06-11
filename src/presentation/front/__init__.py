from fastapi import APIRouter

from .main.router import main

front_router = APIRouter(tags=["Static Pages"])
front_router.include_router(main)
