from typing import TypeVar, Generic
from pydantic import BaseModel, Field, EmailStr, SecretStr
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
