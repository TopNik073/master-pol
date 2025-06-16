from typing import Annotated

from fastapi import Depends

from src.infrastructure.database.connection import DB_DEP
from src.infrastructure.database.repositories import ProductsRepo
from src.presentation.api.admin.v1.products.service import AdminProductsService


async def get_products_service(session: DB_DEP) -> AdminProductsService:
    return AdminProductsService(ProductsRepo(session))


ADMIN_PRODUCTS_SERVICE_DEP = Annotated[
    AdminProductsService, Depends(get_products_service)
]
