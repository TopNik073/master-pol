from fastapi import APIRouter

from .main.router import main

front_router = APIRouter()
front_router.include_router(main)
