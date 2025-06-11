from typing import Annotated
from fastapi import Depends

from src.presentation.api.v1.auth.service import AuthService
from src.infrastructure.database.repositories import UsersRepo
from src.infrastructure.database.connection import DB_DEP


async def get_auth_service(session: DB_DEP):
    return AuthService(UsersRepo(session))


AUTH_SERVICE_DEP = Annotated[AuthService, Depends(get_auth_service)]
