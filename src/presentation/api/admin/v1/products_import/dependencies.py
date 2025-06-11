from typing import Annotated

from fastapi import Depends

from src.infrastructure.database.connection import DB_DEP
from src.infrastructure.database.repositories import ProductsImportRepo
from src.presentation.api.admin.v1.products_import.service import (
    AdminProductsImportService,
)


async def get_products_import_service(session: DB_DEP) -> AdminProductsImportService:
    return AdminProductsImportService(ProductsImportRepo(session))


ADMIN_PRODUCTS_IMPORT_SERVICE_DEP = Annotated[
    AdminProductsImportService, Depends(get_products_import_service)
]
