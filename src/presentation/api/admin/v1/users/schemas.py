from pydantic import BaseModel, EmailStr

from src.infrastructure.database.enums.roles import Roles
from src.presentation.api.v1.schemas import PaginationMetadata, UserBase


class AdminUsersPaginatedResponseSchema(BaseModel):
    items: list[UserBase]
    meta: PaginationMetadata


class AdminUsersControlRequestSchema(BaseModel):
    email: EmailStr
    password: str | None
    name: str
    role: Roles
