from fastapi import APIRouter

from src.presentation.api.v1.guards.jwt import CURRENT_USER_DEP
from src.presentation.api.v1.schemas import SuccessResponseSchema, UserBase
from src.presentation.api.v1.users.dependencies import USER_SERVICE_DEP
from src.presentation.api.v1.users.schemas import UserControlRequestSchema

users = APIRouter(prefix="/users", tags=["Users"])


@users.get("/me")
async def me(current_user: CURRENT_USER_DEP) -> SuccessResponseSchema[UserBase]:
    return SuccessResponseSchema[UserBase](
        data=UserBase(**current_user.dump_to_dict()), message="User was found"
    )


@users.put("/me")
async def update_me(
    service: USER_SERVICE_DEP,
    current_user: CURRENT_USER_DEP,
    data: UserControlRequestSchema,
) -> SuccessResponseSchema[UserBase]:
    user = await service.update(current_user.id, data)
    return SuccessResponseSchema[UserBase](
        data=UserBase(**user.dump_to_dict()),
        message="User profile updated successfully",
    )
