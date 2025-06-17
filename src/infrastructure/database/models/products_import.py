import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base_model import BaseModel

if TYPE_CHECKING:
    from src.infrastructure.database.models.products import Products
    from src.infrastructure.database.models.products_types import ProductsTypes


class ProductsImport(BaseModel):
    __tablename__ = "products_import"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
        unique=True,
    )

    type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products_types.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    article: Mapped[str] = mapped_column(nullable=False)
    minimum_cost: Mapped[float] = mapped_column(nullable=False)

    product_type: Mapped["ProductsTypes"] = relationship(
        back_populates="import_products", passive_deletes=True
    )
    products: Mapped[list["Products"]] = relationship(
        back_populates="product_import",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
