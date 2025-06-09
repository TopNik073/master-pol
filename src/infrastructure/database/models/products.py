from typing import TYPE_CHECKING
from src.infrastructure.database.models.base_model import BaseModel

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey

import datetime
import uuid

if TYPE_CHECKING:
    from src.infrastructure.database.models.partners import Partners


class Products(BaseModel):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4(), unique=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    partner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("partners.id"), nullable=False)
    quantity_products: Mapped[int] = mapped_column(nullable=False)
    sell_date: Mapped[datetime.datetime] = mapped_column(nullable=False)

    partner: Mapped["Partners"] = relationship(back_populates="products")
