import uuid
import bcrypt

from src.infrastructure.admin.service import BaseAdminService

from src.infrastructure.database.models import Users

from src.presentation.api.v1.users.schemas import UserControlRequestSchema

UTF_8_ENCODING = "utf-8"

class UserService(BaseAdminService):
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(UTF_8_ENCODING), bcrypt.gensalt()).decode(
            UTF_8_ENCODING
        )
    async def update(self, id: uuid.UUID, data: UserControlRequestSchema) -> Users:
        if not data.password:
            del data.password
        else:
            data.password = self.hash_password(data.password)

        return await self._repo.update(id, **data.model_dump())
