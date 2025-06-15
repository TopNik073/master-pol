import uuid

from fastapi import APIRouter

from src.presentation.api.admin.v1.products_import.dependencies import (
    ADMIN_PRODUCTS_IMPORT_SERVICE_DEP,
)
from src.presentation.api.v1.guards.jwt import CURRENT_ADMIN_USER_DEP
from src.presentation.api.v1.dependencies import PAGINATED_REQUEST_DEP

from src.presentation.api.v1.schemas import (
    SuccessResponseSchema,
    ProductsImportBase,
    ProductsTypesBase,
    PaginationMetadata,
)
from src.presentation.api.admin.v1.products_import.schemas import (
    AdminProductsImportPaginatedResponseSchema,
    AdminProductsImportControlRequestSchema,
)

admin_products_import = APIRouter(prefix="/products-import", tags=["Products Import"])


@admin_products_import.get("/")
async def get_products_import(
    service: ADMIN_PRODUCTS_IMPORT_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    pagination: PAGINATED_REQUEST_DEP,
) -> SuccessResponseSchema[AdminProductsImportPaginatedResponseSchema]:
    products_import, total = await service.get_paginated(**pagination.dump_to_dict())
    return SuccessResponseSchema[AdminProductsImportPaginatedResponseSchema](
        data=AdminProductsImportPaginatedResponseSchema(
            items=[
                ProductsImportBase(
                    id=product_import.id,
                    type_id=product_import.type_id,
                    name=product_import.name,
                    article=product_import.article,
                    minimum_cost=product_import.minimum_cost,
                    product_type=ProductsTypesBase(
                        id=product_import.product_type.id,
                        name=product_import.product_type.name,
                        coefficient=product_import.product_type.coefficient,
                    ),
                )
                for product_import in products_import
            ],
            meta=PaginationMetadata(
                total=total, page=pagination.page, per_page=pagination.per_page
            ),
        ),
        message="Products Import fetched successfully",
    )


@admin_products_import.get("/{id}")
async def get_products_import_by_id(
    service: ADMIN_PRODUCTS_IMPORT_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[ProductsImportBase]:
    product_import = await service.get(id)
    return SuccessResponseSchema[ProductsImportBase](
        data=ProductsImportBase(
            id=product_import.id,
            type_id=product_import.type_id,
            name=product_import.name,
            article=product_import.article,
            minimum_cost=product_import.minimum_cost,
            product_type=ProductsTypesBase(
                id=product_import.product_type.id,
                name=product_import.product_type.name,
                coefficient=product_import.product_type.coefficient,
            ),
        ),
        message="Product Import fetched by id successfully",
    )


@admin_products_import.post("/")
async def create_product_import(
    service: ADMIN_PRODUCTS_IMPORT_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    product_import: AdminProductsImportControlRequestSchema,
) -> SuccessResponseSchema[ProductsImportBase]:
    product_import = await service.create(product_import)
    return SuccessResponseSchema[ProductsImportBase](
        data=ProductsImportBase(
            id=product_import.id,
            type_id=product_import.type_id,
            name=product_import.name,
            article=product_import.article,
            minimum_cost=product_import.minimum_cost,
            product_type=ProductsTypesBase(
                id=product_import.product_type.id,
                name=product_import.product_type.name,
                coefficient=product_import.product_type.coefficient,
            ),
        ),
        message="Product Import created successfully",
    )


@admin_products_import.put("/{id}")
async def update_product_import(
    service: ADMIN_PRODUCTS_IMPORT_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    product_import: AdminProductsImportControlRequestSchema,
    id: uuid.UUID,
) -> SuccessResponseSchema[ProductsImportBase]:
    product_import = await service.update(id, product_import)
    return SuccessResponseSchema[ProductsImportBase](
        data=ProductsImportBase(
            id=product_import.id,
            type_id=product_import.type_id,
            name=product_import.name,
            article=product_import.article,
            minimum_cost=product_import.minimum_cost,
            product_type=ProductsTypesBase(
                id=product_import.product_type.id,
                name=product_import.product_type.name,
                coefficient=product_import.product_type.coefficient,
            ),
        ),
        message="Product Import updated successfully",
    )


@admin_products_import.delete("/{id}")
async def delete_product_import(
    service: ADMIN_PRODUCTS_IMPORT_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[uuid.UUID]:
    product_import_id = await service.delete(id)
    return SuccessResponseSchema[uuid.UUID](
        data=product_import_id, message="Product Import deleted successfully"
    )
