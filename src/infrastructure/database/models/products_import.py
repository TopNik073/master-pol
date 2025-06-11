from typing import TYPE_CHECKING
from src.infrastructure.database.models.base_model import BaseModel

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey

import uuid

if TYPE_CHECKING:
    from src.infrastructure.database.models.products_types import ProductsTypes
    from src.infrastructure.database.models.products import Products


class ProductsImport(BaseModel):
    __tablename__ = "products_import"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4(),
        unique=True,
    )

    type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products_types.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    article: Mapped[str] = mapped_column(nullable=False)
    minimum_cost: Mapped[float] = mapped_column(nullable=False)

    product_type: Mapped["ProductsTypes"] = relationship(
        back_populates="import_products"
    )
    products: Mapped[list["Products"]] = relationship(back_populates="product_import")
