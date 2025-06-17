import uuid
from datetime import UTC, datetime, timedelta
from typing import Literal

from fastapi import HTTPException
from jose import jwt

from src.core.config import config


class JWTHandler:
    def __init__(self, algorithm: str = "HS256"):
        self.algorithm = algorithm

    def encode(
        self, id: uuid.UUID, token_type: Literal["access", "refresh"]
    ) -> tuple[str, datetime]:
        current_time: datetime = datetime.now(tz=UTC)
        if token_type == "access":
            exp_delta: timedelta = timedelta(minutes=config.ACCESS_TOKEN_EXP_MIN)
        else:
            exp_delta: timedelta = timedelta(minutes=config.REFRESH_TOKEN_EXP_MIN)

        expires_at: datetime = current_time + exp_delta

        jwt_data = {
            "sub": str(id),
            "type": token_type,
            "exp": int(expires_at.timestamp()),
        }

        token = jwt.encode(jwt_data, str(config.JWT_SECRET), self.algorithm)

        return token, expires_at

    def decode(self, token: str):
        try:
            return jwt.decode(token, str(config.JWT_SECRET), self.algorithm)
        except:
            raise HTTPException(403, "Invalid token")

    def validate_token(
        self, token: str, token_type: Literal["access", "refresh"] | None
    ):
        token = self.decode(token)
        if token_type and token["type"] != token_type:
            raise ValueError(
                f"Invalid token token. Expected {token_type}, but {token['type']} was given"
            )

        if datetime.fromtimestamp(token["exp"], tz=UTC) < datetime.now(tz=UTC):
            raise ValueError("Token expired")

        uuid.UUID(token["sub"])

        return token
