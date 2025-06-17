import uuid
from datetime import datetime

from pydantic import BaseModel

from src.presentation.api.v1.schemas import PaginationMetadata, ProductsExtendedSchema


class AdminProductsPaginatedResponseSchema(BaseModel):
    items: list[ProductsExtendedSchema]
    meta: PaginationMetadata


class AdminProductControlRequestSchema(BaseModel):
    quantity_products: int
    sell_date: datetime
    partner_id: uuid.UUID | None
    product_import_id: uuid.UUID | None
