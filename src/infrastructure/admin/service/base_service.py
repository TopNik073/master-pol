import uuid
from typing import TypeVar, Literal
from pydantic import BaseModel as PydanticBaseModel

from fastapi import HTTPException

from src.infrastructure.database.repositories.base_repo import AbstractRepo
from src.infrastructure.admin.service.abstract_service import AbstractAdminService
from src.infrastructure.database.models import BaseModel

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
        return await self._repo.get_filter_by(id=id)

    async def create(self, data: PYDANTIC_MODEL_T) -> BASE_MODEL_T:
        return await self._repo.create(**data.model_dump())

    async def update(self, data: PYDANTIC_MODEL_T) -> BASE_MODEL_T:
        return await self._repo.update(**data.model_dump())

    async def delete(self, id: uuid.UUID) -> uuid.UUID:
        if self._repo.delete(id):
            return id

        raise HTTPException(418, "Can't delete this entity")
