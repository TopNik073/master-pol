from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import config

engine = create_async_engine(
    config.POSTGRES_URL, echo=config.SQLALCHEMY_ECHO, future=True
)

AsyncSessionMaker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting a database session"""
    async with AsyncSessionMaker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


DB_DEP = Annotated[AsyncSession, Depends(get_db)]
