import uuid
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.logger import get_logger
from src.infrastructure.database.enums.roles import Roles
from src.infrastructure.database.models import Users
from src.infrastructure.security.jwt import JWTHandler
from src.presentation.api.v1.users.dependencies import USER_SERVICE_DEP

if TYPE_CHECKING:
    from src.presentation.api.v1.users.service import UserService

logger = get_logger(__name__)

security = HTTPBearer()
jwt_handler = JWTHandler()


async def get_user_from_token(
    credentials: HTTPAuthorizationCredentials, user_service: "UserService"
) -> Users:
    try:
        token = credentials.credentials
        payload = jwt_handler.validate_token(token, "access")

        user = await user_service.get(uuid.UUID(payload["sub"]))
        if not user:
            raise HTTPException(status_code=403, detail="Invalid credentials")
        logger.debug(f"User {user.id} logged in")
        return user
    except ValueError as e:
        logger.error(f"Something went wrong with JWT auth flow.", exc_info=e)
        raise HTTPException(403, detail=str(e))


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_service: USER_SERVICE_DEP,
) -> Users:
    return await get_user_from_token(credentials, user_service)


async def get_current_admin_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_service: USER_SERVICE_DEP,
) -> Users:
    user: Users = await get_user_from_token(credentials, user_service)
    if user.role != Roles.admin:
        raise HTTPException(403, "You haven't admin permissions")

    return user


CURRENT_USER_DEP = Annotated[Users, Depends(get_current_user)]
CURRENT_ADMIN_USER_DEP = Annotated[Users, Depends(get_current_admin_user)]
