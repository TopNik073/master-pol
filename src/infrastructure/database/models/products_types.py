from typing import TYPE_CHECKING
from src.infrastructure.database.models.base_model import BaseModel

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

import uuid

if TYPE_CHECKING:
    from src.infrastructure.database.models.products_import import ProductsImport


class ProductsTypes(BaseModel):
    __tablename__ = "products_types"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
        unique=True,
    )

    name: Mapped[str] = mapped_column(nullable=False)
    coefficient: Mapped[float] = mapped_column(nullable=False)

    import_products: Mapped[list["ProductsImport"]] = relationship(
        back_populates="product_type",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
