from typing import Annotated

from fastapi import Depends

from src.infrastructure.database.connection import DB_DEP
from src.infrastructure.database.repositories import ProductsTypesRepo
from src.presentation.api.admin.v1.products_types.service import (
    AdminProductsTypesService,
)


async def get_products_types_service(session: DB_DEP):
    return AdminProductsTypesService(ProductsTypesRepo(session))


ADMIN_PRODUCTS_TYPES_SERVICE_DEP = Annotated[
    AdminProductsTypesService, Depends(get_products_types_service)
]
