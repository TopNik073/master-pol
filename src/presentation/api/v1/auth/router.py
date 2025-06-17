from fastapi import APIRouter

from src.presentation.api.v1.auth.dependencies import AUTH_SERVICE_DEP
from src.presentation.api.v1.auth.schemas import (
    AuthResponseSchema,
    LoginRequestSchema,
    RefreshTokenRequest,
    RegisterRequestSchema,
)
from src.presentation.api.v1.schemas import SuccessResponseSchema

auth = APIRouter(prefix="/auth", tags=["Auth"])


@auth.post("/register", response_model=SuccessResponseSchema[AuthResponseSchema])
async def register(
    user: RegisterRequestSchema, service: AUTH_SERVICE_DEP
) -> SuccessResponseSchema[AuthResponseSchema]:
    user = await service.register(user)
    return SuccessResponseSchema[AuthResponseSchema](
        data=user, message="User registered"
    )


@auth.post("/login", response_model=SuccessResponseSchema[AuthResponseSchema])
async def login(
    user: LoginRequestSchema, service: AUTH_SERVICE_DEP
) -> SuccessResponseSchema[AuthResponseSchema]:
    user = await service.login(user)
    return SuccessResponseSchema[AuthResponseSchema](
        data=user, message="User logged in"
    )


@auth.post("/refresh", response_model=SuccessResponseSchema[AuthResponseSchema])
async def refresh(
    refresh_token: RefreshTokenRequest, service: AUTH_SERVICE_DEP
) -> SuccessResponseSchema[AuthResponseSchema]:
    user = await service.refresh(refresh_token)
    return SuccessResponseSchema[AuthResponseSchema](
        data=user, message="Tokens are refreshed"
    )
