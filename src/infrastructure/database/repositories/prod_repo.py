from typing import Literal

from src.infrastructure.database.repositories.base_repo import PostgresRepo
from src.infrastructure.database.models import Products, Partners, ProductsImport, ProductsTypes

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
            selectinload(Products.partner),
            selectinload(Products.product_import).selectinload(ProductsImport.product_type),
        )

        subq = select(self.model.id)

        if search_query:
            search_conditions = []
            for column in self.model.__table__.columns:
                if isinstance(column.type, (String, Text)):
                    search_conditions.append(column.ilike(f"%{search_query}%"))

            if search_query:
                subq = subq.join(Products.partner).join(Products.product_import).join(ProductsImport.product_type)
                search_conditions.extend([
                    Partners.name.ilike(f"%{search_query}%"),
                    ProductsImport.name.ilike(f"%{search_query}%"),
                    ProductsTypes.name.ilike(f"%{search_query}%")
                ])
                subq = subq.where(or_(*search_conditions))

        stmt = stmt.where(self.model.id.in_(subq))

        if order_by:
            order_mapping = {
                "quantity_products": Products.quantity_products,
                "sell_date": Products.sell_date,
                "partner_name": Partners.name,
                "partner_type": Partners.partner_type,
                "partner_rate": Partners.rate,
                "product_name": ProductsImport.name,
                "product_article": ProductsImport.article,
                "product_minimum_cost": ProductsImport.minimum_cost,
                "product_type_name": ProductsTypes.name,
                "product_type_coefficient": ProductsTypes.coefficient,
            }

            if order_by in order_mapping:
                column = order_mapping[order_by]
                stmt = stmt.order_by(
                    desc(column) if order_direction == "desc" else asc(column)
                )

        count_stmt = select(func.count()).select_from(subq)
        total = await self._session.scalar(count_stmt)

        stmt = stmt.limit(per_page).offset((page - 1) * per_page)

        result = await self._session.execute(stmt)
        items = result.scalars().all()

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
