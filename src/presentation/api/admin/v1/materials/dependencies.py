from typing import Annotated
from fastapi import Depends

from src.infrastructure.database.connection import DB_DEP

from src.infrastructure.database.repositories import MaterialsRepo
from src.presentation.api.admin.v1.materials.service import AdminMaterialsService


async def get_admin_materials_service(session: DB_DEP):
    return AdminMaterialsService(MaterialsRepo(session))


ADMIN_MATERIALS_SERVICE_DEP = Annotated[AdminMaterialsService, Depends(get_admin_materials_service)]
