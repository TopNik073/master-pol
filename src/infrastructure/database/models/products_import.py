from src.infrastructure.database.models.base_model import BaseModel
from products_types import Products_types

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID

import uuid


class ProductsImport(BaseModel):
    __tablename__ = "products_import"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(), primary_key=True, nullable=False, default=uuid.uuid4()
    )

    type: Mapped[Products_types.id] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    article: Mapped[str] = mapped_column(nullable=False)
    minimum_cost: Mapped[float] = mapped_column(nullable=False)
