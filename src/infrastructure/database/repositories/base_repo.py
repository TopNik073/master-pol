import uuid
from abc import ABC, abstractmethod
from typing import Any, Literal, TypeVar

from sqlalchemy import String, Text, asc, delete, desc, func, or_, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, joinedload

from src.infrastructure.database.models import BaseModel

MODEL_T = TypeVar("MODEL_T", bound=BaseModel)


class AbstractRepo(ABC):
    @abstractmethod
    async def get_by_filter(
        self,
        mode: Literal["one", "all"],
        load_relationships: list[str] | None = None,
        **filters,
    ):
        """Get record by filters"""
        raise NotImplemented("This method isn't implemented yet")

    @abstractmethod
    async def get_paginated(
        self,
        page: int,
        per_page: int,
        search_query: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] = "asc",
        include: list[str] | None = None,
    ):
        """Get paginated records with search, order and relationships"""
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

    @staticmethod
    @abstractmethod
    async def execute_sql_script(
        session: AsyncSession, sql_script: str, commit: bool = True
    ) -> Any:
        """
        Execute raw SQL script and return results.

        Args:
            session (AsyncSession): session for executing
            sql_script (str): SQL script to execute
            commit (bool): Whether to commit the transaction. Defaults to True.

        Returns:
            Any: Query results. For SELECT queries returns list of dicts,
                 for other queries returns execution result.
        """
        raise NotImplemented("This method isn't implemented yet")


class PostgresRepo(AbstractRepo):
    def __init__(self, model: MODEL_T, session: AsyncSession):
        self.model = model
        self._session = session

    async def get_by_filter(
        self,
        mode: Literal["one", "all"],
        load_relationships: list[str] | None = None,
        **filters,
    ):
        query = select(self.model)

        # Add relationship loading if specified
        if load_relationships:
            for relationship in load_relationships:
                query = query.options(joinedload(getattr(self.model, relationship)))

        # Add filters
        for k, v in filters.items():
            query = query.where(getattr(self.model, k) == v)

        result = await self._session.execute(query)
        result = result.scalars().unique().all()

        if len(result) == 0:
            return

        if mode == "one":
            return result[0]

        return result

    async def get_paginated(
        self,
        page: int,
        per_page: int,
        search_query: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] = "asc",
        include: list[str] | None = None,
    ) -> tuple[list[MODEL_T], int]:
        stmt = select(self.model)

        if include:
            for relation in include:
                if hasattr(self.model, relation):
                    stmt = stmt.options(joinedload(getattr(self.model, relation)))

        if search_query:
            search_conditions = []
            for column in self.model.__table__.columns:
                if isinstance(column.type, (String, Text)):
                    if hasattr(column.type, "enums"):
                        try:
                            enum_values = [
                                e
                                for e in column.type.enums
                                if search_query.lower() in e.lower()
                            ]
                            if enum_values:
                                search_conditions.append(column.in_(enum_values))
                        except:
                            continue
                    else:
                        search_conditions.append(column.ilike(f"%{search_query}%"))

            if search_conditions:
                stmt = stmt.where(or_(*search_conditions))

        if order_by:
            column = getattr(self.model, order_by, None)
            if column is not None and isinstance(column, InstrumentedAttribute):
                stmt = stmt.order_by(
                    desc(column) if order_direction == "desc" else asc(column)
                )

        # Apply pagination
        stmt = stmt.limit(per_page).offset((page - 1) * per_page)

        # Get items
        result = await self._session.execute(stmt)
        items = result.unique().scalars().all()

        # Get total count
        count_stmt = select(func.count()).select_from(self.model)
        if search_query and search_conditions:
            count_stmt = count_stmt.where(or_(*search_conditions))

        total_result = await self._session.execute(count_stmt)
        total = total_result.scalar_one()

        return items, total

    async def create(self, **data):
        model = self.model(**data)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)

        return model

    async def update(self, id: uuid.UUID, **data):
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        result = await self._session.execute(query)
        model = result.scalar_one()

        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def delete(self, id: uuid.UUID):
        query = delete(self.model).where(self.model.id == id)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.rowcount > 0

    @staticmethod
    async def execute_sql_script(
        session: AsyncSession, sql_script: str, commit: bool = False
    ) -> Any:
        """
        Execute raw SQL script and return results.

        Args:
            session (AsyncSession): session for executing
            sql_script (str): SQL script to execute
            commit (bool): Whether to commit the transaction. Defaults to True.

        Returns:
            Any: Query results. For SELECT queries returns list of dicts,
                 for other queries returns execution result.
        """
        result = await session.execute(text(sql_script))

        if commit:
            await session.commit()

        if sql_script.strip().upper().startswith("SELECT"):
            return [dict(row) for row in result]

        return result
