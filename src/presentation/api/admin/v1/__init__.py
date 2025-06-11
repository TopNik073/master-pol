from fastapi import APIRouter

from .partners.router import admin_partners as admin_partners_router
from .users.router import admin_users as admin_users_router
from .products_types.router import admin_product_types as admin_product_types_router
from .products_import.router import (
    admin_products_import as admin_products_import_router,
)

admin_v1 = APIRouter(prefix="/v1")

admin_v1.include_router(admin_partners_router)
admin_v1.include_router(admin_users_router)
admin_v1.include_router(admin_product_types_router)
admin_v1.include_router(admin_products_import_router)
