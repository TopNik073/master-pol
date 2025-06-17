from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import Materials
from src.infrastructure.database.repositories.base_repo import PostgresRepo


class MaterialsRepo(PostgresRepo):
    """Materials Repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(model=Materials, session=session)
