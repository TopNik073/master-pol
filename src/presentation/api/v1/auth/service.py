import uuid
import bcrypt
from fastapi import HTTPException

from src.infrastructure.database.repositories import UsersRepo
from src.infrastructure.database.models import Users
from src.infrastructure.database.enums.roles import Roles
from src.infrastructure.security.jwt import JWTHandler

from src.presentation.api.v1.auth.schemas import (
    RegisterRequestSchema,
    LoginRequestSchema,
    AuthResponseSchema,
    TokensPairSchema,
    TokenSchema,
    RefreshTokenRequest,
    UserBase,
)

UTF_8_ENCODING: str = "utf-8"


class AuthService:
    def __init__(self, user_repo: UsersRepo):
        self.user_repo = user_repo
        self.jwt_handler = JWTHandler()

    def create_auth_response(self, user: Users):
        access_token, access_exp = self.jwt_handler.encode(user.id, "access")
        refresh_token, refresh_exp = self.jwt_handler.encode(user.id, "refresh")

        return AuthResponseSchema(
            user=UserBase(**user.dump_to_dict()),
            tokens=TokensPairSchema(
                access=TokenSchema(token=access_token, expires_at=access_exp),
                refresh=TokenSchema(token=refresh_token, expires_at=refresh_exp),
            ),
        )

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(UTF_8_ENCODING), bcrypt.gensalt()).decode(
            UTF_8_ENCODING
        )

    @staticmethod
    def validate_password(password: str, req_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(UTF_8_ENCODING),
            req_password.encode(UTF_8_ENCODING),
        )

    async def register(self, user: RegisterRequestSchema) -> AuthResponseSchema | None:
        if await self.user_repo.get_by_filter("one", email=user.email):
            raise HTTPException(status_code=400, detail="User already exists")

        user_obj: Users = Users(
            email=user.email,
            name=user.name,
            role=Roles.user,
            password=self.hash_password(user.password),
        )

        users_res = await self.user_repo.create(**user_obj.dump_to_dict())
        return self.create_auth_response(users_res)

    async def login(self, user: LoginRequestSchema) -> AuthResponseSchema | None:
        res: Users = await self.user_repo.get_by_filter("one", email=user.email)
        if res:
            if self.validate_password(user.password, res.password):
                return self.create_auth_response(res)

        raise HTTPException(status_code=401, detail="Invalid credentials")

    async def refresh(self, refresh_token: RefreshTokenRequest) -> AuthResponseSchema:
        token = self.jwt_handler.validate_token(refresh_token.token, "refresh")
        user = await self.user_repo.get_by_filter("one", id=uuid.UUID(token["sub"]))
        return self.create_auth_response(user)
