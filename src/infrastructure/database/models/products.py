from src.infrastructure.database.models.base_model import BaseModel
from partners import Partners

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID

import datetime
import uuid


class Products(BaseModel):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(), primary_key=True, nullable=False, default=uuid.uuid4()
    )

    name: Mapped[str] = mapped_column(nullable=False)
    partner: Mapped[Partners.id] = mapped_column(nullable=False)
    quantity_products: Mapped[int] = mapped_column(nullable=False)
    sell_date: Mapped[datetime.datetime] = mapped_column(nullable=False)
