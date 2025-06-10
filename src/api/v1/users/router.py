from fastapi import APIRouter

from src.api.v1.guards.jwt_guard import CURRENT_USER_DEP

from src.api.v1.schemas import SuccessResponseSchema, UserBase


users = APIRouter(prefix="/users", tags=["users"])


@users.get("/me")
async def me(current_user: CURRENT_USER_DEP) -> SuccessResponseSchema[UserBase]:
    return SuccessResponseSchema[UserBase](
        data=UserBase(**current_user.dump_to_dict()), message="User was found"
    )
