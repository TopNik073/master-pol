import uuid

from fastapi import APIRouter

from src.presentation.api.admin.v1.users.dependencies import ADMIN_USER_SERVICE_DEP
from src.presentation.api.v1.guards.jwt import CURRENT_ADMIN_USER_DEP
from src.presentation.api.v1.dependencies import PAGINATED_REQUEST_DEP

from src.presentation.api.v1.schemas import (
    SuccessResponseSchema,
    PaginationMetadata,
    UserBase,
)
from src.presentation.api.admin.v1.users.schemas import (
    AdminUsersPaginatedResponseSchema,
    AdminUsersControlRequestSchema,
)

admin_users = APIRouter(prefix="/users", tags=["Users Admin"])


@admin_users.get("/")
async def get_users(
    service: ADMIN_USER_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    pagination: PAGINATED_REQUEST_DEP,
) -> SuccessResponseSchema[AdminUsersPaginatedResponseSchema]:
    users, total = await service.get_paginated(**pagination.dump_to_dict())
    return SuccessResponseSchema[AdminUsersPaginatedResponseSchema](
        data=AdminUsersPaginatedResponseSchema(
            items=[UserBase(**user.dump_to_dict()) for user in users],
            meta=PaginationMetadata(
                total=total,
                page=pagination.page,
                per_page=pagination.per_page,
            ),
        ),
        message="Users fetched successfully",
    )


@admin_users.get("/{id}")
async def get_user_by_id(
    service: ADMIN_USER_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[UserBase]:
    user = await service.get(id)
    return SuccessResponseSchema[UserBase](
        data=UserBase(**user.dump_to_dict()), message="User fetched by id successfully"
    )


@admin_users.post("/")
async def create_user(
    service: ADMIN_USER_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    user: AdminUsersControlRequestSchema,
) -> SuccessResponseSchema[UserBase]:
    user = await service.create(user)
    return SuccessResponseSchema[UserBase](
        data=UserBase(**user.dump_to_dict()), message="User registered successfully"
    )


@admin_users.put("/{id}")
async def update_user(
    service: ADMIN_USER_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    user: AdminUsersControlRequestSchema,
    id: uuid.UUID,
) -> SuccessResponseSchema[UserBase]:
    user = await service.update(id, user)
    return SuccessResponseSchema[UserBase](
        data=UserBase(**user.dump_to_dict()), message="User updated successfully"
    )


@admin_users.delete("/{id}")
async def delete_user(
    service: ADMIN_USER_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[uuid.UUID]:
    user_id = await service.delete(id)
    return SuccessResponseSchema[uuid.UUID](data=user_id, message="User deleted successfully")
