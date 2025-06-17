from fastapi import HTTPException

from src.infrastructure.admin.service import BaseAdminService
from src.infrastructure.database.enums.partner_statuses import PartnerStatuses
from src.infrastructure.database.models import Partners
from src.presentation.api.admin.v1.partners_bid.schemas import PartnerBidBase


class AdminPartnersBidService(BaseAdminService):
    async def create(self, data: PartnerBidBase) -> Partners:
        if await self._repo.get_by_filter("one", email=data.email):
            raise HTTPException(400, "This bid (or partner) already exist")

        partner = Partners(**data.model_dump())
        partner.rate = 5.0
        partner.status = PartnerStatuses.pending

        return await self._repo.create(**partner.dump_to_dict())
