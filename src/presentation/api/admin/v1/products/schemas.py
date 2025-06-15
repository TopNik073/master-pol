import uuid

from pydantic import BaseModel
from datetime import datetime

from src.presentation.api.v1.schemas import ProductsExtendedSchema, PaginationMetadata


class AdminProductsPaginatedResponseSchema(BaseModel):
    items: list[ProductsExtendedSchema]
    meta: PaginationMetadata


class AdminProductControlRequestSchema(BaseModel):
    quantity_products: int
    sell_date: datetime
    partner_id: uuid.UUID | None
    product_import_id: uuid.UUID | None
