from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import config

async_engine = create_async_engine(config.POSTGRES_URL, echo=config.SQLALCHEMY_ECHO, future=True)


async def get_db():
    async with async_sessionmaker(
        async_engine, autoflush=False, expire_on_commit=False, autocommit=False
    ) as session:
        try:
            yield session
        except:
            await session.rollback()
        finally:
            await session.close()

DB_DEP = Annotated[AsyncSession, Depends(get_db)]
