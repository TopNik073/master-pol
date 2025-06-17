from fastapi import HTTPException

from src.core.config import config
from src.core.logger import get_logger
from src.infrastructure.database.connection import AsyncSessionMaker
from src.infrastructure.database.enums.roles import Roles
from src.infrastructure.database.repositories import UsersRepo
from src.presentation.api.admin.v1.users.schemas import AdminUsersControlRequestSchema
from src.presentation.api.admin.v1.users.service import AdminUsersService

logger = get_logger(__name__)


async def create_admin():
    try:
        if not config.ADMIN_EMAIL or not config.ADMIN_PASSWORD:
            logger.warning("Admin credentials not found!")
            return
        admin = AdminUsersControlRequestSchema(
            email=config.ADMIN_EMAIL,
            password=config.ADMIN_PASSWORD,
            name=config.ADMIN_NAME,
            role=Roles.admin,
        )

        async with AsyncSessionMaker() as session:
            repo = UsersRepo(session)
            service = AdminUsersService(repo)
            await service.create(admin)

        logger.info("Admin user created successfully")
    except HTTPException:
        logger.info("Admin user already exist")
