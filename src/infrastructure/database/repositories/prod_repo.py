from typing import Literal

from src.infrastructure.database.repositories.base_repo import PostgresRepo
from src.infrastructure.database.models import Products

from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select, func, or_, desc, asc, String, Text

from sqlalchemy.ext.asyncio import AsyncSession


class ProductsRepo(PostgresRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Products, session=session)

    async def get_paginated(
        self,
        page: int,
        per_page: int,
        search_query: str | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
        include: list[str] | None = None,
    ) -> tuple[list[Products], int]:
        stmt = select(self.model).options(
            selectinload(self.model.partner),
            selectinload(self.model.product_import).selectinload(
                self.model.product_import.property.mapper.class_.product_type
            ),
        )

        # Add joins for sorting and searching
        stmt = (
            stmt.join(self.model.partner)
            .join(self.model.product_import)
            .join(self.model.product_import.property.mapper.class_.product_type)
        )

        if search_query:
            search_conditions = []
            # Search in Products table
            for column in self.model.__table__.columns:
                if isinstance(column.type, (String, Text)):
                    search_conditions.append(column.ilike(f"%{search_query}%"))

            # Search in related tables
            search_conditions.extend(
                [
                    self.model.partner.property.mapper.class_.name.ilike(
                        f"%{search_query}%"
                    ),
                    self.model.product_import.property.mapper.class_.name.ilike(
                        f"%{search_query}%"
                    ),
                    self.model.product_import.property.mapper.class_.product_type.property.mapper.class_.name.ilike(
                        f"%{search_query}%"
                    ),
                ]
            )

            if search_conditions:
                stmt = stmt.where(or_(*search_conditions))

        if order_by:
            # Define mapping for order_by fields
            order_mapping = {
                # Products table fields
                "quantity_products": self.model.quantity_products,
                "sell_date": self.model.sell_date,
                # Partner fields
                "partner_name": self.model.partner.property.mapper.class_.name,
                "partner_type": self.model.partner.property.mapper.class_.partner_type,
                "partner_rate": self.model.partner.property.mapper.class_.rate,
                # Product import fields
                "product_name": self.model.product_import.property.mapper.class_.name,
                "product_article": self.model.product_import.property.mapper.class_.article,
                "product_minimum_cost": self.model.product_import.property.mapper.class_.minimum_cost,
                # Product type fields
                "product_type_name": self.model.product_import.property.mapper.class_.product_type.property.mapper.class_.name,
                "product_type_coefficient": self.model.product_import.property.mapper.class_.product_type.property.mapper.class_.coefficient,
            }

            column = order_mapping.get(order_by)
            if column is not None:
                stmt = stmt.order_by(
                    desc(column) if order_direction == "desc" else asc(column)
                )

        count_stmt = select(func.count()).select_from(self.model)
        if search_query:
            count_stmt = (
                count_stmt.join(self.model.partner)
                .join(self.model.product_import)
                .join(self.model.product_import.property.mapper.class_.product_type)
            )
            if search_conditions:
                count_stmt = count_stmt.where(or_(*search_conditions))
        total = await self._session.scalar(count_stmt)

        stmt = stmt.limit(per_page).offset((page - 1) * per_page)

        result = await self._session.execute(stmt)
        items = result.unique().scalars().all()

        return items, total

    async def get_by_filter(
        self,
        mode: Literal["one", "all"],
        load_relationships: list[str] | None = None,
        **filters,
    ):
        query = select(self.model).options(
            selectinload(self.model.partner),
            selectinload(self.model.product_import).selectinload(
                self.model.product_import.property.mapper.class_.product_type
            ),
        )

        for k, v in filters.items():
            query = query.where(getattr(self.model, k) == v)

        result = await self._session.execute(query)
        result = result.scalars().unique().all()

        if len(result) == 0:
            return

        if mode == "one":
            return result[0]

        return result
