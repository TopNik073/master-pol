import uuid
from typing import Literal

from src.infrastructure.admin.service import BaseAdminService
from src.infrastructure.database.models import Products


class AdminProductsService(BaseAdminService):
    async def get_paginated(
        self,
        page: int,
        per_page: int,
        search_query: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] = "asc",
    ) -> tuple[list[Products], int]:
        return await self._repo.get_paginated(
            page,
            per_page,
            search_query,
            order_by,
            order_direction,
            ["partner", "product_import", "product_import.product_type"],
        )

    async def get(self, id: uuid.UUID) -> Products:
        return await self._repo.get_by_filter(
            "one",
            id=id,
            load_relationships=[
                "partner",
                "product_import",
                "product_import.product_type",
            ],
        )
