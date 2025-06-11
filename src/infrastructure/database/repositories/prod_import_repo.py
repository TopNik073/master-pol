from src.infrastructure.database.repositories.base_repo import PostgresRepo
from src.infrastructure.database.models import ProductsImport

from sqlalchemy.ext.asyncio import AsyncSession


class ProductsImportRepo(PostgresRepo):
    """Products Import Repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(model=ProductsImport, session=session)
