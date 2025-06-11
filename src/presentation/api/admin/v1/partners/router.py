import uuid

from fastapi import APIRouter

from src.presentation.api.admin.v1.partners.dependencies import (
    ADMIN_PARTNERS_SERVICE_DEP,
)
from src.presentation.api.v1.guards.jwt import CURRENT_ADMIN_USER_DEP
from src.presentation.api.v1.dependencies import PAGINATED_REQUEST_DEP

from src.presentation.api.v1.schemas import SuccessResponseSchema
from src.presentation.api.admin.v1.partners.schemas import (
    AdminPartnersPaginatedResponseSchema,
    PartnerBase,
    PaginationMetadata,
    AdminControlPartnerRequest,
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
            partners=[PartnerBase(**partner.dump_to_dict()) for partner in partners],
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
        data=PartnerBase(**partner), message="Partner fetched by id successfully"
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


@admin_partners.put("/")
async def update_partner(
    service: ADMIN_PARTNERS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    partner: AdminControlPartnerRequest,
) -> SuccessResponseSchema[PartnerBase]:
    partner = await service.update(partner)
    return SuccessResponseSchema[PartnerBase](
        data=partner.dump_to_dict(), message="Partner updated successfully"
    )


@admin_partners.delete("/")
async def delete_partner(
    service: ADMIN_PARTNERS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[uuid.UUID]:
    partner_id: uuid.UUID = await service.delete(id)
    return SuccessResponseSchema[uuid.UUID](data=partner_id, message="Partner deleted successfully")
