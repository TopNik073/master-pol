from src.infrastructure.database.repositories.base_repo import PostgresRepo
from src.infrastructure.database.models import Users

from sqlalchemy.ext.asyncio import AsyncSession


class UsersRepo(PostgresRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Users, session=session)
