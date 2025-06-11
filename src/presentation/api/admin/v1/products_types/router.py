import uuid

from fastapi import APIRouter

from src.presentation.api.admin.v1.products_types.dependencies import (
    ADMIN_PRODUCTS_TYPES_SERVICE_DEP,
)
from src.presentation.api.v1.guards.jwt import CURRENT_ADMIN_USER_DEP
from src.presentation.api.v1.dependencies import PAGINATED_REQUEST_DEP

from src.presentation.api.v1.schemas import SuccessResponseSchema, PaginationMetadata
from src.presentation.api.admin.v1.products_types.schemas import (
    AdminProductsTypesPaginatedResponseSchema,
    ProductsTypesBase,
    AdminControlProductsTypesRequestSchema,
)

admin_product_types = APIRouter(prefix="/products-types", tags=["Products Types"])


@admin_product_types.get("/")
async def get_products_types(
    service: ADMIN_PRODUCTS_TYPES_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    pagination: PAGINATED_REQUEST_DEP,
) -> SuccessResponseSchema[AdminProductsTypesPaginatedResponseSchema]:
    prod_types, total = await service.get_paginated(**pagination.dump_to_dict())
    return SuccessResponseSchema[AdminProductsTypesPaginatedResponseSchema](
        data=AdminProductsTypesPaginatedResponseSchema(
            products_types=[
                ProductsTypesBase(**prod_type.dump_to_dict()) for prod_type in prod_types
            ],
            meta=PaginationMetadata(
                total=total, page=pagination.page, per_page=pagination.per_page
            ),
        ),
        message="Products types fetched successfully",
    )


@admin_product_types.get("/{id}")
async def get_products_type_by_id(
    service: ADMIN_PRODUCTS_TYPES_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[ProductsTypesBase]:
    product_type = await service.get(id)
    return SuccessResponseSchema[ProductsTypesBase](
        data=ProductsTypesBase(**product_type.dump_to_dict()),
        message="Product Type fetched by id successfully",
    )


@admin_product_types.post("/")
async def create_product_type(
    service: ADMIN_PRODUCTS_TYPES_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    prod_type: AdminControlProductsTypesRequestSchema,
) -> SuccessResponseSchema[ProductsTypesBase]:
    prod_type = await service.create(prod_type)
    return SuccessResponseSchema[ProductsTypesBase](
        data=ProductsTypesBase(**prod_type.dump_to_dict()),
        message="Product Type created successfully",
    )


@admin_product_types.put("/")
async def update_product_type(
    service: ADMIN_PRODUCTS_TYPES_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    prod_type: AdminControlProductsTypesRequestSchema,
) -> SuccessResponseSchema[ProductsTypesBase]:
    prod_type = await service.update(prod_type)
    return SuccessResponseSchema[ProductsTypesBase](
        data=ProductsTypesBase(**prod_type.dump_to_dict()),
        message="Product Type updated successfully",
    )


@admin_product_types.delete("/")
async def delete_product_type(
    service: ADMIN_PRODUCTS_TYPES_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[uuid.UUID]:
    prod_type_id = await service.delete(id)
    return SuccessResponseSchema[uuid.UUID](
        data=prod_type_id, message="Product Type deleted successfully"
    )
