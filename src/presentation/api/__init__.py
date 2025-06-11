from fastapi import APIRouter

from .v1 import v1_router
from .admin import admin as admin_router

api_router = APIRouter(prefix="/api")

api_router.include_router(v1_router)
api_router.include_router(admin_router)
