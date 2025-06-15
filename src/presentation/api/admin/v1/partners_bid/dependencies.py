from typing import Annotated
from fastapi import Depends

from src.infrastructure.database.connection import DB_DEP

from src.infrastructure.database.repositories import PartnersBidRepo
from src.presentation.api.admin.v1.partners_bid.service import AdminPartnersBidService


async def get_admin_partners_service(session: DB_DEP):
    return AdminPartnersBidService(PartnersBidRepo(session))


ADMIN_PARTNERS_BID_SERVICE_DEP = Annotated[
    AdminPartnersBidService, Depends(get_admin_partners_service)
]
