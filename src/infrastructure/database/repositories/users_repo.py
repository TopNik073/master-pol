from typing import Literal

from src.infrastructure.database.repositories.base_repo import PostgresRepo
from src.infrastructure.database.models import Users

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, InstrumentedAttribute
from sqlalchemy import select, func, or_, asc, desc, String, Text


class UsersRepo(PostgresRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Users, session=session)

    async def get_paginated(
        self,
        page: int,
        per_page: int,
        search_query: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] = "asc",
        include: list[str] | None = None,
    ) -> tuple[list[Users], int]:
        stmt = select(self.model)

        if include:
            for relation in include:
                if hasattr(self.model, relation):
                    stmt = stmt.options(joinedload(getattr(self.model, relation)))

        if search_query:
            search_conditions = []
            for column in self.model.__table__.columns:
                if isinstance(column.type, (String, Text)) and column.name != "password":
                    if hasattr(column.type, "enums"):
                        try:
                            enum_values = [
                                e for e in column.type.enums if search_query.lower() in e.lower()
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
                stmt = stmt.order_by(desc(column) if order_direction == "desc" else asc(column))

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
