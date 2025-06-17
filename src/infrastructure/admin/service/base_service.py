import uuid
from typing import Literal, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel as PydanticBaseModel

from src.infrastructure.admin.service.abstract_service import AbstractAdminService
from src.infrastructure.database.models import BaseModel
from src.infrastructure.database.repositories.base_repo import AbstractRepo

ABSTRACT_REPO_T = TypeVar("ABSTRACT_REPO_T", bound=AbstractRepo)
BASE_MODEL_T = TypeVar("BASE_MODEL_T", bound=BaseModel)
PYDANTIC_MODEL_T = TypeVar("PYDANTIC_MODEL_T", bound=PydanticBaseModel)


class BaseAdminService(AbstractAdminService):
    def __init__(self, repo: ABSTRACT_REPO_T):
        self._repo = repo

    async def get_paginated(
        self,
        page: int,
        per_page: int,
        search_query: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] = "asc",
    ) -> tuple[list[BASE_MODEL_T], int]:
        return await self._repo.get_paginated(
            page, per_page, search_query, order_by, order_direction
        )

    async def get(self, id: uuid.UUID) -> BASE_MODEL_T:
        return await self._repo.get_by_filter("one", id=id)

    async def create(self, data: PYDANTIC_MODEL_T) -> BASE_MODEL_T:
        return await self._repo.create(**data.model_dump())

    async def update(self, id: uuid.UUID, data: PYDANTIC_MODEL_T) -> BASE_MODEL_T:
        return await self._repo.update(id, **data.model_dump())

    async def delete(self, id: uuid.UUID) -> uuid.UUID:
        if await self._repo.delete(id):
            return id

        raise HTTPException(418, "Can't delete this entity")
