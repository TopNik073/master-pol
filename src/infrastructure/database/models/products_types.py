from src.infrastructure.database.models.base_model import BaseModel

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID

import uuid


class ProductsTypes(BaseModel):
    __tablename__ = "products_types"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(), primary_key=True, nullable=False, default=uuid.uuid4()
    )
    name: Mapped[str] = mapped_column(nullable=False)
    coefficient: Mapped[float] = mapped_column(nullable=False)
