import uuid

from fastapi import APIRouter

from src.presentation.api.admin.v1.partners_bid.dependencies import (
    ADMIN_PARTNERS_BID_SERVICE_DEP,
)
from src.presentation.api.admin.v1.partners_bid.schemas import (
    AdminPartnerBidPaginatedResponseSchema,
    PartnersBidCreateRequestSchema,
    AdminPartnersBidUpdateRequestSchema,
    PartnerBidExtendedSchema,
)
from src.presentation.api.v1.dependencies import PAGINATED_REQUEST_DEP
from src.presentation.api.v1.guards.jwt import CURRENT_ADMIN_USER_DEP
from src.presentation.api.v1.schemas import PaginationMetadata, SuccessResponseSchema

admin_partners_bid = APIRouter(prefix="/partners-bid", tags=["Partners (Bid)"])


@admin_partners_bid.post("/")
async def get_bid_request(
    service: ADMIN_PARTNERS_BID_SERVICE_DEP, data: PartnersBidCreateRequestSchema
) -> SuccessResponseSchema[uuid.UUID]:
    partner = await service.create(data)
    return SuccessResponseSchema[uuid.UUID](data=partner.id, message="Bid created successfully")


@admin_partners_bid.get("/")
async def get_partners_bid_paginated(
    service: ADMIN_PARTNERS_BID_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    pagination: PAGINATED_REQUEST_DEP,
) -> SuccessResponseSchema[AdminPartnerBidPaginatedResponseSchema]:
    partners_bid, total = await service.get_paginated(**pagination.dump_to_dict())
    return SuccessResponseSchema[AdminPartnerBidPaginatedResponseSchema](
        data=AdminPartnerBidPaginatedResponseSchema(
            items=[
                PartnerBidExtendedSchema(**partner_bid.dump_to_dict())
                for partner_bid in partners_bid
            ],
            meta=PaginationMetadata(
                page=pagination.page, per_page=pagination.per_page, total=total
            ),
        ),
        message="Partners (bid) fetched successfully",
    )


@admin_partners_bid.get("/{id}")
async def get_partner_bid(
    service: ADMIN_PARTNERS_BID_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[PartnerBidExtendedSchema]:
    partner_bid = await service.get(id)
    return SuccessResponseSchema[PartnerBidExtendedSchema](
        data=PartnerBidExtendedSchema(**partner_bid.dump_to_dict()),
        message="Partner (bid) fetched successfully",
    )


@admin_partners_bid.put("/{id}")
async def update_partner_bid(
    service: ADMIN_PARTNERS_BID_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    data: AdminPartnersBidUpdateRequestSchema,
    id: uuid.UUID,
) -> SuccessResponseSchema[PartnerBidExtendedSchema]:
    partner_bid = await service.update(id, data)
    return SuccessResponseSchema[PartnerBidExtendedSchema](
        data=PartnerBidExtendedSchema(**partner_bid.dump_to_dict()),
        message="Partner (bid) updated successfully",
    )


@admin_partners_bid.delete("/{id}")
async def delete_partner_bid(
    service: ADMIN_PARTNERS_BID_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    id: uuid.UUID,
) -> SuccessResponseSchema[uuid.UUID]:
    partner_bid_id = await service.delete(id)
    return SuccessResponseSchema[uuid.UUID](
        data=partner_bid_id, message="Partner (bid) successfully deleted"
    )
