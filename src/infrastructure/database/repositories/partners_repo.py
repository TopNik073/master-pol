from sqlalchemy import String, Text, asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.infrastructure.database.enums.partner_statuses import PartnerStatuses
from src.infrastructure.database.models.partners import Partners
from src.infrastructure.database.repositories.base_repo import PostgresRepo


class PartnersRepo(PostgresRepo):
    """Partners Repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(model=Partners, session=session)

    async def get_paginated(
        self,
        page: int,
        per_page: int,
        search_query: str | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
        include: list[str] | None = None,
    ) -> tuple[list[Partners], int]:
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.products)
                .selectinload(self.model.products.property.mapper.class_.product_import)
                .selectinload(
                    self.model.products.property.mapper.class_.product_import.property.mapper.class_.product_type
                )
            )
            .where(self.model.status == PartnerStatuses.active)
        )

        if search_query:
            search_conditions = []
            for column in self.model.__table__.columns:
                if isinstance(column.type, (String, Text)) and column.name != "status":
                    search_conditions.append(column.ilike(f"%{search_query}%"))
            if search_conditions:
                stmt = stmt.where(or_(*search_conditions))

        if order_by:
            column = getattr(self.model, order_by, None)
            if column is not None:
                stmt = stmt.order_by(
                    desc(column) if order_direction == "desc" else asc(column)
                )

        count_stmt = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.status == PartnerStatuses.active)
        )
        if search_query and search_conditions:
            count_stmt = count_stmt.where(or_(*search_conditions))
        total = await self._session.scalar(count_stmt)

        stmt = stmt.limit(per_page).offset((page - 1) * per_page)

        result = await self._session.execute(stmt)
        items = result.unique().scalars().all()

        return items, total
