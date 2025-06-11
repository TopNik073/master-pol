from pydantic import BaseModel, EmailStr

from src.presentation.api.v1.schemas import PartnerBase, PaginationMetadata


class AdminPartnersPaginatedResponseSchema(BaseModel):
    partners: list[PartnerBase]
    meta: PaginationMetadata


class AdminControlPartnerRequest(BaseModel):
    partner_type: str
    name: str
    email: EmailStr
    ur_address: str
    director: str
    phone_number: str
    inn: int
    rate: int
