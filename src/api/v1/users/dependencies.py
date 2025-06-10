from typing import Annotated

from fastapi import Depends

from src.infrastructure.database.connection import DB_DEP
from src.infrastructure.database.repositories import UsersRepo
from src.api.v1.users.user_service import UserService


async def get_user_service(session: DB_DEP) -> UserService:
    return UserService(UsersRepo(session))


USER_SERVICE_DEP = Annotated[UserService, Depends(get_user_service)]
