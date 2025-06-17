import uuid

from fastapi import APIRouter

from src.presentation.api.admin.v1.products.dependencies import (
    ADMIN_PRODUCTS_SERVICE_DEP,
)
from src.presentation.api.admin.v1.products.schemas import (
    AdminProductControlRequestSchema,
    AdminProductsPaginatedResponseSchema,
)
from src.presentation.api.v1.dependencies import PAGINATED_REQUEST_DEP
from src.presentation.api.v1.guards.jwt import CURRENT_ADMIN_USER_DEP
from src.presentation.api.v1.schemas import (
    PaginationMetadata,
    PartnerBase,
    ProductsBase,
    ProductsExtendedSchema,
    ProductsImportBase,
    ProductsTypesBase,
    SuccessResponseSchema,
)

admin_products = APIRouter(prefix="/products", tags=["Products"])


@admin_products.get("/")
async def get_products(
    service: ADMIN_PRODUCTS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    pagination: PAGINATED_REQUEST_DEP,
) -> SuccessResponseSchema[AdminProductsPaginatedResponseSchema]:
    products, total = await service.get_paginated(**pagination.dump_to_dict())
    return SuccessResponseSchema[AdminProductsPaginatedResponseSchema](
        data=AdminProductsPaginatedResponseSchema(
            items=[
                ProductsExtendedSchema(
                    id=product.id,
                    quantity_products=product.quantity_products,
                    sell_date=product.sell_date,
                    partner=(
                        PartnerBase(**product.partner.dump_to_dict())
                        if product.partner
                        else None
                    ),
                    product_import=(
                        ProductsImportBase(
                            id=product.product_import.id,
                            type_id=product.product_import.type_id,
                            name=product.product_import.name,
                            article=product.product_import.article,
                            minimum_cost=product.product_import.minimum_cost,
                            product_type=(
                                ProductsTypesBase(
                                    id=product.product_import.product_type.id,
                                    name=product.product_import.product_type.name,
                                    coefficient=product.product_import.product_type.coefficient,
                                )
                                if product.product_import.product_type
                                else None
                            ),
                        )
                        if product.product_import
                        else None
                    ),
                )
                for product in products
            ],
            meta=PaginationMetadata(
                total=total, page=pagination.page, per_page=pagination.per_page
            ),
        ),
        message="Products fetched successfully",
    )


@admin_products.get("/{id}")
async def get_product(
    service: ADMIN_PRODUCTS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[ProductsExtendedSchema]:
    product = await service.get(id)
    return SuccessResponseSchema[ProductsExtendedSchema](
        data=ProductsExtendedSchema(
            id=product.id,
            quantity_products=product.quantity_products,
            sell_date=product.sell_date,
            partner=(
                PartnerBase(**product.partner.dump_to_dict())
                if product.partner
                else None
            ),
            product_import=(
                ProductsImportBase(
                    id=product.product_import.id,
                    type_id=product.product_import.type_id,
                    name=product.product_import.name,
                    article=product.product_import.article,
                    minimum_cost=product.product_import.minimum_cost,
                    product_type=(
                        ProductsTypesBase(
                            id=product.product_import.product_type.id,
                            name=product.product_import.product_type.name,
                            coefficient=product.product_import.product_type.coefficient,
                        )
                        if product.product_import.product_type
                        else None
                    ),
                )
                if product.product_import
                else None
            ),
        ),
        message="Product fetched successfully",
    )


@admin_products.post("/")
async def create_product(
    service: ADMIN_PRODUCTS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    product: AdminProductControlRequestSchema,
) -> SuccessResponseSchema[ProductsBase]:
    product = await service.create(product)
    return SuccessResponseSchema[ProductsBase](
        data=ProductsBase(**product.dump_to_dict()),
        message="Product created successfully",
    )


@admin_products.put("/{id}")
async def update_product(
    service: ADMIN_PRODUCTS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    product: AdminProductControlRequestSchema,
    id: uuid.UUID,
) -> SuccessResponseSchema[ProductsBase]:
    product = await service.update(id, product)
    return SuccessResponseSchema[ProductsBase](
        data=ProductsBase(**product.dump_to_dict()),
        message="Product updated successfully",
    )


@admin_products.delete("/{id}")
async def delete_product(
    service: ADMIN_PRODUCTS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[uuid.UUID]:
    product_id = await service.delete(id)
    return SuccessResponseSchema[uuid.UUID](
        data=product_id, message="Product deleted successfully"
    )
