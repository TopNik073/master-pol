from typing import Literal, Optional, List, Type
import uuid
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload, joinedload, relationship


class AbstractRepo(ABC):
    @abstractmethod
    async def get_by_filter(
            self,
            mode: Literal["one", "all"],
            load_relationships: Optional[List[str]] = None,
            **filters
    ):
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
    def __init__(self, model: Type, session: AsyncSession):
        self.model = model
        self._session = session

    async def get_by_filter(
            self,
            mode: Literal["one", "all"],
            load_relationships: Optional[List[str]] = None,
            **filters
    ):
        query = select(self.model)

        # Add relationship loading if specified
        if load_relationships:
            for relationship in load_relationships:
                query = query.options(selectinload(getattr(self.model, relationship)))

        # Add filters
        for k, v in filters.items():
            query = query.where(getattr(self.model, k) == v)

        result = await self._session.execute(query)

        if mode == "one":
            return result.scalar_one()

        return result.scalars().unique().all()

    async def create(self, **data):
        relationship_data = {}
        for key, value in data.items():
            if hasattr(self.model, key) and isinstance(getattr(self.model, key).property, relationship):
                relationship_data[key] = value
                del data[key]

        model = self.model(**data)

        # Set relationship data
        for key, value in relationship_data.items():
            setattr(model, key, value)

        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)

        return model

    async def update(self, id: uuid.UUID, **data):
        relationship_data = {}
        for key, value in data.items():
            if hasattr(self.model, key) and isinstance(getattr(self.model, key).property, relationship):
                relationship_data[key] = value
                del data[key]

        query = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
        result = await self._session.execute(query)
        model = result.scalar_one()

        # Update relationship data
        for key, value in relationship_data.items():
            setattr(model, key, value)

        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def delete(self, id: uuid.UUID):
        query = delete(self.model).where(self.model.id == id)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.rowcount > 0
