from sqlalchemy import String, Text, asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.infrastructure.database.models import ProductsImport
from src.infrastructure.database.repositories.base_repo import PostgresRepo


class ProductsImportRepo(PostgresRepo):
    """Products Import Repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(model=ProductsImport, session=session)
