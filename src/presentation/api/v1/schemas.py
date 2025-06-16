from typing import TypeVar, Generic
from pydantic import BaseModel, Field, EmailStr
import uuid

from datetime import datetime

from src.infrastructure.database.enums.partner_statuses import PartnerStatuses
from src.infrastructure.database.enums.roles import Roles

T = TypeVar("T")


class SuccessResponseSchema(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: T
    error: str | None = None


class ErrorResponseSchema(BaseModel):
    success: bool = False
    message: str
    error: str


class UserBase(BaseModel):
    id: uuid.UUID
    name: str = Field(..., min_length=2)
    email: EmailStr
    role: Roles


class PartnerBase(BaseModel):
    id: uuid.UUID
    partner_type: str
    name: str
    email: EmailStr
    ur_address: str
    director: str
    phone_number: str
    inn: int
    rate: float
    status: PartnerStatuses


class PartnerBidBase(BaseModel):
    id: uuid.UUID
    partner_type: str
    name: str
    email: EmailStr
    ur_address: str
    director: str
    phone_number: str
    inn: int


class ProductsTypesBase(BaseModel):
    id: uuid.UUID
    name: str
    coefficient: float


class ProductsImportBase(BaseModel):
    id: uuid.UUID
    type_id: uuid.UUID
    name: str
    article: str
    minimum_cost: float
    product_type: ProductsTypesBase


class ProductsBase(BaseModel):
    id: uuid.UUID
    quantity_products: int
    sell_date: datetime


class ProductsExtendedSchema(ProductsBase):
    partner: PartnerBase
    product_import: ProductsImportBase


class PartnersProductsExtendedSchema(PartnerBase):
    products: list[ProductsExtendedSchema]
    discount: float


class MaterialsBase(BaseModel):
    id: uuid.UUID
    name: str
    defect_rate_percent: float


class PaginationMetadata(BaseModel):
    total: int
    page: int
    per_page: int
