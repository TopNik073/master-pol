from typing import Literal

import uuid

from src.infrastructure.database.repositories import UsersRepo
from src.infrastructure.database.models import Users


class UserService:
    def __init__(self, user_repo: UsersRepo):
        self.user_repo = user_repo

    async def find_by_id(
        self, id: uuid.UUID, mode: Literal["one", "all"]
    ) -> Users | None:
        return await self.user_repo.get_by_filter(mode, id=id)
