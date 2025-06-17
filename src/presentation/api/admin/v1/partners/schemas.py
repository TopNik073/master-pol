from pydantic import BaseModel, EmailStr

from src.infrastructure.database.enums.partner_statuses import PartnerStatuses
from src.presentation.api.v1.schemas import (
    PaginationMetadata,
    PartnerBase,
    PartnersProductsExtendedSchema,
)


class AdminPartnersPaginatedResponseSchema(BaseModel):
    items: list[PartnersProductsExtendedSchema]
    meta: PaginationMetadata


class AdminControlPartnerRequest(BaseModel):
    partner_type: str
    name: str
    email: EmailStr
    ur_address: str
    director: str
    phone_number: str
    inn: int
    rate: float
    status: PartnerStatuses
