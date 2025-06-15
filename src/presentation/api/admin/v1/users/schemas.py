from pydantic import BaseModel, EmailStr

from src.presentation.api.v1.schemas import PaginationMetadata, UserBase

from src.infrastructure.database.enums.roles import Roles


class AdminUsersPaginatedResponseSchema(BaseModel):
    items: list[UserBase]
    meta: PaginationMetadata


class AdminUsersControlRequestSchema(BaseModel):
    email: EmailStr
    password: str | None
    name: str
    role: Roles
