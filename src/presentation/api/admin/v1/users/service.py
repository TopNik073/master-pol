import uuid

import bcrypt
from fastapi import HTTPException

from src.infrastructure.admin.service import BaseAdminService
from src.infrastructure.database.models import Users
from src.presentation.api.admin.v1.users.schemas import AdminUsersControlRequestSchema

UTF_8_ENCODING = "utf-8"


class AdminUsersService(BaseAdminService):
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(UTF_8_ENCODING), bcrypt.gensalt()).decode(
            UTF_8_ENCODING
        )

    @staticmethod
    def validate_password(password: str, req_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(UTF_8_ENCODING),
            req_password.encode(UTF_8_ENCODING),
        )

    async def create(self, data: AdminUsersControlRequestSchema) -> Users:
        if await self._repo.get_by_filter("one", email=data.email):
            raise HTTPException(400, "User already exist")

        if not data.password or len(data.password) < 6:
            raise HTTPException(400, "Password must be 6 symbols length minimum")

        data.password = self.hash_password(data.password)
        return await self._repo.create(**data.model_dump())

    async def update(
        self, id: uuid.UUID, data: AdminUsersControlRequestSchema
    ) -> Users:
        if data.password and len(data.password) < 6:
            raise HTTPException(400, "Password must be 6 symbols length minimum")
        else:
            data.password = self.hash_password(data.password)

        return await self._repo.update(id, **data.model_dump())
