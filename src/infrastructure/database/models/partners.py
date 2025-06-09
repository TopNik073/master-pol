from src.infrastructure.database.models.base_model import BaseModel

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID

import uuid


class Partners(BaseModel):
    __tablename__ = "partners"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(), primary_key=True, nullable=False, default=uuid.uuid4()
    )

    partner_type: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    director: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    ur_address: Mapped[str] = mapped_column(nullable=False)
    inn: Mapped[int] = mapped_column(nullable=False)
    rate: Mapped[float] = mapped_column(nullable=False)
