from pydantic import BaseModel

from src.presentation.api.v1.schemas import PaginationMetadata, ProductsTypesBase


class AdminProductsTypesPaginatedResponseSchema(BaseModel):
    items: list[ProductsTypesBase]
    meta: PaginationMetadata


class AdminControlProductsTypesRequestSchema(BaseModel):
    name: str
    coefficient: float
