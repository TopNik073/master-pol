from pydantic import BaseModel

from src.presentation.api.v1.schemas import ProductsTypesBase, PaginationMetadata


class AdminProductsTypesPaginatedResponseSchema(BaseModel):
    products_types: list[ProductsTypesBase]
    meta: PaginationMetadata


class AdminControlProductsTypesRequestSchema(BaseModel):
    name: str
    coefficient: float
