from pydantic import BaseModel

from src.presentation.api.v1.auth.schemas import RegisterRequestSchema
from src.presentation.api.v1.schemas import PaginationMetadata, UserBase


class AdminUsersPaginatedResponseSchema(BaseModel):
    users: list[UserBase]
    meta: PaginationMetadata
