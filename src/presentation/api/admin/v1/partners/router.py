import uuid

from fastapi import APIRouter

from src.presentation.api.admin.v1.partners.dependencies import (
    ADMIN_PARTNERS_SERVICE_DEP,
)
from src.presentation.api.admin.v1.partners.schemas import (
    AdminControlPartnerRequest,
    AdminPartnersPaginatedResponseSchema,
    PaginationMetadata,
    PartnerBase,
    PartnersProductsExtendedSchema,
)
from src.presentation.api.v1.dependencies import PAGINATED_REQUEST_DEP
from src.presentation.api.v1.guards.jwt import CURRENT_ADMIN_USER_DEP
from src.presentation.api.v1.schemas import (
    ProductsExtendedSchema,
    ProductsImportBase,
    ProductsTypesBase,
    SuccessResponseSchema,
)

admin_partners = APIRouter(prefix="/partners", tags=["Partners"])


@admin_partners.get("/")
async def get_partners(
    service: ADMIN_PARTNERS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    pagination: PAGINATED_REQUEST_DEP,
) -> SuccessResponseSchema[AdminPartnersPaginatedResponseSchema]:
    """Get paginated partners"""
    partners, total = await service.get_paginated(**pagination.dump_to_dict())
    return SuccessResponseSchema[AdminPartnersPaginatedResponseSchema](
        data=AdminPartnersPaginatedResponseSchema(
            items=[
                PartnersProductsExtendedSchema(
                    id=partner.id,
                    partner_type=partner.partner_type,
                    name=partner.name,
                    email=partner.email,
                    ur_address=partner.ur_address,
                    director=partner.director,
                    phone_number=partner.phone_number,
                    inn=partner.inn,
                    rate=partner.rate,
                    discount=partner.discount,
                    status=partner.status,
                    products=[
                        ProductsExtendedSchema(
                            id=prod.id,
                            quantity_products=prod.quantity_products,
                            sell_date=prod.sell_date,
                            partner=(
                                PartnerBase(**partner.dump_to_dict())
                                if prod.partner
                                else None
                            ),
                            product_import=(
                                ProductsImportBase(
                                    id=prod.product_import.id,
                                    type_id=prod.product_import.type_id,
                                    name=prod.product_import.name,
                                    article=prod.product_import.article,
                                    minimum_cost=prod.product_import.minimum_cost,
                                    product_type=(
                                        ProductsTypesBase(
                                            id=prod.product_import.product_type.id,
                                            name=prod.product_import.product_type.name,
                                            coefficient=prod.product_import.product_type.coefficient,
                                        )
                                        if prod.product_import.product_type
                                        else None
                                    ),
                                )
                                if prod.product_import
                                else None
                            ),
                        )
                        for prod in partner.products
                    ],
                )
                for partner in partners
            ],
            meta=PaginationMetadata(
                total=total,
                page=pagination.page,
                per_page=pagination.per_page,
            ),
        ),
        message="Successfully get partners",
    )


@admin_partners.get("/{id}")
async def get_partner_by_id(
    service: ADMIN_PARTNERS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[PartnerBase]:
    partner = await service.get(id)
    return SuccessResponseSchema[PartnerBase](
        data=PartnerBase(**partner.dump_to_dict()),
        message="Partner fetched by id successfully",
    )


@admin_partners.post("/")
async def create_partner(
    service: ADMIN_PARTNERS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    partner: AdminControlPartnerRequest,
) -> SuccessResponseSchema[PartnerBase]:
    partner = await service.create(partner)
    return SuccessResponseSchema[PartnerBase](
        data=PartnerBase(**partner.dump_to_dict()),
        message="Partner created successfully",
    )


@admin_partners.put("/{id}")
async def update_partner(
    service: ADMIN_PARTNERS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    partner: AdminControlPartnerRequest,
    id: uuid.UUID,
) -> SuccessResponseSchema[PartnerBase]:
    partner = await service.update(id, partner)
    return SuccessResponseSchema[PartnerBase](
        data=PartnerBase(**partner.dump_to_dict()),
        message="Partner updated successfully",
    )


@admin_partners.delete("/{id}")
async def delete_partner(
    service: ADMIN_PARTNERS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[uuid.UUID]:
    partner_id: uuid.UUID = await service.delete(id)
    return SuccessResponseSchema[uuid.UUID](
        data=partner_id, message="Partner deleted successfully"
    )
