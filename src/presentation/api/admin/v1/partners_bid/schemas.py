import uuid

from pydantic import BaseModel, EmailStr

from src.infrastructure.database.enums.partner_statuses import PartnerStatuses
from src.presentation.api.v1.schemas import PaginationMetadata, PartnerBidBase


class PartnerBidExtendedSchema(PartnerBidBase):
    rate: int
    status: PartnerStatuses


class AdminPartnerBidPaginatedResponseSchema(BaseModel):
    items: list[PartnerBidExtendedSchema]
    meta: PaginationMetadata


class AdminPartnersBidControlRequestSchema(BaseModel):
    partner_type: str
    name: str
    email: EmailStr
    ur_address: str
    director: str
    phone_number: str
    inn: int
    rate: int
    status: PartnerStatuses
