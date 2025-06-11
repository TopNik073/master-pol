import uuid
from pydantic import BaseModel

from src.presentation.api.v1.schemas import PaginationMetadata, ProductsImportBase


class AdminProductsImportPaginatedResponseSchema(BaseModel):
    products_import: list[ProductsImportBase]
    meta: PaginationMetadata


class AdminProductsImportControlRequestSchema(BaseModel):
    type_id: uuid.UUID
    name: str
    article: str
    minimum_cost: float
