from typing import Annotated
import uuid

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.logger import get_logger
from src.infrastructure.security.jwt import JWTHandler
from src.infrastructure.database.models import Users
from src.api.v1.users.dependencies import USER_SERVICE_DEP

logger = get_logger(__name__)

security = HTTPBearer()
jwt_handler = JWTHandler()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_service: USER_SERVICE_DEP,
) -> Users:
    try:
        token = credentials.credentials
        payload = jwt_handler.validate_token(token, "access")

        user = await user_service.find_by_id(uuid.UUID(payload["sub"]), "one")
        if not user:
            raise HTTPException(status_code=403, detail="Invalid credentials")
        logger.debug(f"User {user.id} logged in")
        return user
    except ValueError as e:
        logger.error(f"Something went wrong with JWT auth flow.", exc_info=e)
        raise HTTPException(403, detail=str(e))


CURRENT_USER_DEP = Annotated[Users, Depends(get_current_user)]
