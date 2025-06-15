import uuid
from typing import TypeVar, Literal
from pydantic import BaseModel as PydanticBaseModel
from abc import ABC, abstractmethod

from src.infrastructure.database.models import BaseModel

BASE_MODEL_T = TypeVar("BASE_MODEL_T", bound=BaseModel)
PYDANTIC_MODEL_T = TypeVar("PYDANTIC_MODEL_T", bound=PydanticBaseModel)


class AbstractAdminService(ABC):
    @abstractmethod
    async def get_paginated(
        self,
        page: int,
        per_page: int,
        search_query: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] = "asc",
    ) -> tuple[list[BASE_MODEL_T], int]:
        raise NotImplemented("This method isn't implemented in abstract class")

    @abstractmethod
    async def get(self, id: uuid.UUID) -> BASE_MODEL_T:
        raise NotImplemented("This method isn't implemented in abstract class")

    @abstractmethod
    async def create(self, data: PYDANTIC_MODEL_T) -> BASE_MODEL_T:
        raise NotImplemented("This method isn't implemented in abstract class")

    @abstractmethod
    async def update(self, id: uuid.UUID, data: PYDANTIC_MODEL_T) -> BASE_MODEL_T:
        raise NotImplemented("This method isn't implemented in abstract class")

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> uuid.UUID:
        raise NotImplemented("This method isn't implemented in abstract class")
