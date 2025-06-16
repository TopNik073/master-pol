from typing import Annotated
from fastapi import Depends

from src.infrastructure.database.connection import DB_DEP

from src.infrastructure.database.repositories import PartnersRepo
from src.presentation.api.admin.v1.partners.service import AdminPartnersService


async def get_admin_partners_service(session: DB_DEP):
    return AdminPartnersService(PartnersRepo(session))


ADMIN_PARTNERS_SERVICE_DEP = Annotated[
    AdminPartnersService, Depends(get_admin_partners_service)
]
