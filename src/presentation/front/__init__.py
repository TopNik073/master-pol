from fastapi import APIRouter

from .admin.router import admin_static as admin_static_router
from .main.router import main_static as main_static_router

front_router = APIRouter(tags=["Static Pages"])

front_router.include_router(main_static_router)
front_router.include_router(admin_static_router)
