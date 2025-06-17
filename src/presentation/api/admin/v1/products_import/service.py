import uuid
from typing import Literal

from src.infrastructure.admin.service import BaseAdminService
from src.infrastructure.database.models import ProductsImport
from src.presentation.api.admin.v1.products_import.schemas import (
    AdminProductsImportControlRequestSchema,
)


class AdminProductsImportService(BaseAdminService):
    async def get_paginated(
        self,
        page: int,
        per_page: int,
        search_query: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] = "asc",
    ) -> tuple[list[ProductsImport], int]:
        return await self._repo.get_paginated(
            page, per_page, search_query, order_by, order_direction, ["product_type"]
        )

    async def get(self, id: uuid.UUID) -> ProductsImport:
        return await self._repo.get_by_filter(
            "one", id=id, load_relationships=["product_type"]
        )

    async def update(
        self, id: uuid.UUID, data: AdminProductsImportControlRequestSchema
    ) -> ProductsImport:
        await self._repo.update(id, **data.model_dump())
        return await self.get(id)

    async def create(
        self, data: AdminProductsImportControlRequestSchema
    ) -> ProductsImport:
        product_import = await self._repo.create(**data.model_dump())
        return await self.get(product_import.id)
