from fastapi import APIRouter

from .v1 import admin_v1

admin = APIRouter(prefix="/admin")

admin.include_router(admin_v1)
