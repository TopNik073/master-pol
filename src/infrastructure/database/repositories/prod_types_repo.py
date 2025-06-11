from src.infrastructure.database.repositories.base_repo import PostgresRepo
from src.infrastructure.database.models import ProductsTypes

from sqlalchemy.ext.asyncio import AsyncSession


class ProductsTypesRepo(PostgresRepo):
    """Products Types Repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(model=ProductsTypes, session=session)
