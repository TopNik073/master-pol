from typing import Literal
import uuid
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete


class AbstractRepo(ABC):
    @abstractmethod
    async def get_by_filter(self, mode: Literal["one", "all"], **filters):
        """Get record by filters"""
        raise NotImplemented("This method isn't implemented yet")

    @abstractmethod
    async def create(self, **data):
        """Create a record"""
        raise NotImplemented("This method isn't implemented yet")

    @abstractmethod
    async def update(self, id: uuid.UUID, **data):
        """Update a record"""
        raise NotImplemented("This method isn't implemented yet")

    @abstractmethod
    async def delete(self, id: uuid.UUID):
        """Delete a record (hard)"""
        raise NotImplemented("This method isn't implemented yet")


class PostgresRepo(AbstractRepo):
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self._session = session

    async def get_by_filter(self, mode: Literal["one", "all"], **filters):
        query = select(self.model)
        for k, v in filters.items():
            query = query.where(getattr(self.model, k) == v)

        result = await self._session.execute(query)

        if mode == "one":
            return result.scalar_one()

        return result.scalars().unique().all()

    async def create(self, **data):
        model = self.model(**data)

        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)

        return model

    async def update(self, id: uuid.UUID, **data):
        query = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalar_one()

    async def delete(self, id: uuid.UUID):
        query = delete(self.model).where(self.model.id == id)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.rowcount > 0
