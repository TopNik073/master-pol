from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import ProductsTypes
from src.infrastructure.database.repositories.base_repo import PostgresRepo


class ProductsTypesRepo(PostgresRepo):
    """Products Types Repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(model=ProductsTypes, session=session)
