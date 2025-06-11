from typing import Literal

from src.infrastructure.admin.service import BaseAdminService
from src.infrastructure.database.models import ProductsImport


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
            page, per_page, search_query, order_by, order_direction, ["products_types"]
        )
