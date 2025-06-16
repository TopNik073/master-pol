from pydantic import BaseModel

from src.presentation.api.v1.schemas import MaterialsBase, PaginationMetadata


class AdminMaterialsPaginatedResponse(BaseModel):
    items: list[MaterialsBase]
    meta: PaginationMetadata


class AdminMaterialsControlRequest(BaseModel):
    name: str
    defect_rate_percent: float
