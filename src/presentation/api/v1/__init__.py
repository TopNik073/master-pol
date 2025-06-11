from fastapi import APIRouter

from .auth.router import auth as auth_router
from .users.router import users as users_router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
