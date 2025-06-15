from typing import TYPE_CHECKING
from src.infrastructure.database.models.base_model import BaseModel

from src.infrastructure.database.enums.partner_statuses import PartnerStatuses

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, BIGINT

import uuid

if TYPE_CHECKING:
    from src.infrastructure.database.models.products import Products


class Partners(BaseModel):
    __tablename__ = "partners"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
        unique=True,
    )

    status: Mapped[PartnerStatuses] = mapped_column(nullable=False, default=PartnerStatuses.pending)

    partner_type: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    director: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    ur_address: Mapped[str] = mapped_column(nullable=False)
    inn: Mapped[int] = mapped_column(BIGINT, nullable=False)
    rate: Mapped[float] = mapped_column(nullable=False)

    products: Mapped[list["Products"]] = relationship(back_populates="partner")
