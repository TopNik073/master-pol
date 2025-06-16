import uuid

from fastapi import APIRouter

from src.presentation.api.v1.guards.jwt import CURRENT_ADMIN_USER_DEP
from src.presentation.api.v1.dependencies import PAGINATED_REQUEST_DEP
from src.presentation.api.admin.v1.materials.dependencies import ADMIN_MATERIALS_SERVICE_DEP

from src.presentation.api.v1.schemas import SuccessResponseSchema, MaterialsBase, PaginationMetadata
from src.presentation.api.admin.v1.materials.schemas import (
    AdminMaterialsPaginatedResponse,
    AdminMaterialsControlRequest,
)

admin_materials = APIRouter(prefix="/materials", tags=["Materials"])


@admin_materials.get("/")
async def get_materials(
    service: ADMIN_MATERIALS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    pagination: PAGINATED_REQUEST_DEP,
) -> SuccessResponseSchema[AdminMaterialsPaginatedResponse]:
    materials, total = await service.get_paginated(**pagination.dump_to_dict())
    return SuccessResponseSchema[AdminMaterialsPaginatedResponse](
        data=AdminMaterialsPaginatedResponse(
            items=[MaterialsBase(**material.dump_to_dict()) for material in materials],
            meta=PaginationMetadata(
                page=pagination.page, per_page=pagination.per_page, total=total
            ),
        ),
        message="Materials fetched successfully",
    )


@admin_materials.get("/{id}")
async def get_material(
    service: ADMIN_MATERIALS_SERVICE_DEP, _current_user: CURRENT_ADMIN_USER_DEP, id: uuid.UUID
) -> SuccessResponseSchema[MaterialsBase]:
    material = await service.get(id)
    return SuccessResponseSchema[MaterialsBase](
        data=MaterialsBase(**material.dump_to_dict()), message="Material fetched successfully"
    )


@admin_materials.post("/")
async def create_material(
    service: ADMIN_MATERIALS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    material: AdminMaterialsControlRequest,
) -> SuccessResponseSchema[MaterialsBase]:
    material = await service.create(material)
    return SuccessResponseSchema[MaterialsBase](
        data=MaterialsBase(**material.dump_to_dict()), message="Material created successfully"
    )


@admin_materials.put("/{id}")
async def update_material(
    service: ADMIN_MATERIALS_SERVICE_DEP,
    _current_user: CURRENT_ADMIN_USER_DEP,
    material: AdminMaterialsControlRequest,
    id: uuid.UUID,
) -> SuccessResponseSchema[MaterialsBase]:
    material = await service.update(id, material)
    return SuccessResponseSchema[MaterialsBase](
        data=MaterialsBase(**material.dump_to_dict()), message="Material updated successfully"
    )


@admin_materials.delete("/{id}")
async def delete_material(
    service: ADMIN_MATERIALS_SERVICE_DEP, _current_user: CURRENT_ADMIN_USER_DEP, id: uuid.UUID
) -> SuccessResponseSchema[uuid.UUID]:
    material_id = await service.delete(id)
    return SuccessResponseSchema[uuid.UUID](
        data=material_id, message="Material deleted successfully"
    )
