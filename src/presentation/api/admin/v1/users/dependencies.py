from typing import Annotated

from fastapi import Depends

from src.infrastructure.database.connection import DB_DEP
from src.infrastructure.database.repositories import UsersRepo
from src.presentation.api.admin.v1.users.service import AdminUsersService


def get_admin_users_service(session: DB_DEP):
    return AdminUsersService(UsersRepo(session))


ADMIN_USER_SERVICE_DEP = Annotated[AdminUsersService, Depends(get_admin_users_service)]
