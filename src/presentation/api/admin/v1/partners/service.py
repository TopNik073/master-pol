from typing import Literal

from src.infrastructure.admin.service import BaseAdminService
from src.infrastructure.database.models import Partners


class AdminPartnersService(BaseAdminService):

    @staticmethod
    def calculate_discount(partners: list[Partners]):
        for partner in partners:
            partner_sold = 0
            for product in partner.products:
                partner_sold += product.quantity_products

            if partner_sold < 10_000:
                discount = 0.0

            elif partner_sold < 50_000:
                discount = 0.05

            elif partner_sold < 300_000:
                discount = 0.1

            else:
                discount = 0.15

            partner.discount = discount

    async def get_paginated(
        self,
        page: int,
        per_page: int,
        search_query: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] = "asc",
    ) -> tuple[list[Partners], int]:
        partners, total = await self._repo.get_paginated(
            page,
            per_page,
            search_query,
            order_by,
            order_direction,
            [
                "products",
                "products.product_import",
                "products.product_import.product_type",
            ],
        )
        self.calculate_discount(partners)
        return partners, total
