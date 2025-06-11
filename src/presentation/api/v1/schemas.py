from typing import TypeVar, Generic
from pydantic import BaseModel, Field, EmailStr
import uuid

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
    rate: int
    discount: float


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


class PaginationMetadata(BaseModel):
    total: int
    page: int
    per_page: int
