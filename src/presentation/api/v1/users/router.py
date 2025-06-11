from fastapi import APIRouter

from src.presentation.api.v1.guards.jwt import CURRENT_USER_DEP

from src.presentation.api.v1.schemas import SuccessResponseSchema, UserBase


users = APIRouter(prefix="/users", tags=["Users"])


@users.get("/me")
async def me(current_user: CURRENT_USER_DEP) -> SuccessResponseSchema[UserBase]:
    return SuccessResponseSchema[UserBase](
        data=UserBase(**current_user.dump_to_dict()), message="User was found"
    )
