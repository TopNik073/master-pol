from src.infrastructure.database.repositories.base_repo import PostgresRepo
from src.infrastructure.database.models.partners import Partners

from sqlalchemy.ext.asyncio import AsyncSession


class PartnersRepo(PostgresRepo):
    """Partners Repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(model=Partners, session=session)
