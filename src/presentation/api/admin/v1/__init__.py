from fastapi import APIRouter

from .users.router import admin_users as admin_users_router
from .partners.router import admin_partners as admin_partners_router
from .partners_bid.router import admin_partners_bid as admin_partners_bid_router
from .products.router import admin_products as admin_products_router
from .products_import.router import (
    admin_products_import as admin_products_import_router,
)
from .products_types.router import admin_product_types as admin_product_types_router
from .stats.router import admin_stats as admin_stats_router
from .materials.router import admin_materials as admin_materials_router

admin_v1 = APIRouter(prefix="/v1")

admin_v1.include_router(admin_users_router)
admin_v1.include_router(admin_partners_router)
admin_v1.include_router(admin_partners_bid_router)
admin_v1.include_router(admin_products_router)
admin_v1.include_router(admin_product_types_router)
admin_v1.include_router(admin_products_import_router)
admin_v1.include_router(admin_stats_router)
admin_v1.include_router(admin_materials_router)
