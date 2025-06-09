from src.infrastructure.database.models.base_model import BaseModel

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

import uuid


class Materials(BaseModel):
    __tablename__ = "materials"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4(), unique=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    defect_rate_percent: Mapped[float] = mapped_column(nullable=False)
