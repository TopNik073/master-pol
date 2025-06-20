from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


def get_datetime_UTC() -> datetime:  # noqa: N802
    """Get current UTC datetime"""
    return datetime.now()


class BaseModel(AsyncAttrs, DeclarativeBase):
    """Base class for inheritance new models"""

    repr_cols_num = 1
    repr_cols = ()

    def __repr__(self) -> str:
        """Relationships are not used in repr() because may lead to unexpected lazy loads"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f'<{self.__class__.__name__} {", ".join(cols)}>'

    def dump_to_dict(self) -> dict[str, Any]:
        obj = {}
        for col in self.__table__.columns.keys():
            value = getattr(self, col)
            if value or value == 0:
                obj[col] = value

        return obj
