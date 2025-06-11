from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from src.infrastructure.database.enums.roles import Roles

from src.presentation.api.v1.schemas import UserBase


class AuthRequestSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class RegisterRequestSchema(AuthRequestSchema):
    name: str = Field(..., min_length=2)
    role: Roles


class LoginRequestSchema(AuthRequestSchema): ...


class TokenSchema(BaseModel):
    token: str
    expires_at: datetime


class TokensPairSchema(BaseModel):
    access: TokenSchema
    refresh: TokenSchema


class AuthResponseSchema(BaseModel):
    user: UserBase
    tokens: TokensPairSchema


class RefreshTokenRequest(BaseModel):
    token: str
