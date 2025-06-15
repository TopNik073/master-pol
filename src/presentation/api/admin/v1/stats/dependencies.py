from typing import Annotated

from fastapi import Depends

from src.infrastructure.database.connection import DB_DEP

from src.presentation.api.admin.v1.stats.service import AdminStatsService
from src.infrastructure.database.repositories.base_repo import PostgresRepo


async def get_admin_stats_service(session: DB_DEP) -> AdminStatsService:
    return AdminStatsService(PostgresRepo(None, session), session)


ADMIN_STATS_SERVICE_DEP = Annotated[AdminStatsService, Depends(get_admin_stats_service)]
