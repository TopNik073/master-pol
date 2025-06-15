from fastapi import APIRouter

from src.presentation.api.v1.guards.jwt import CURRENT_ADMIN_USER_DEP
from src.presentation.api.admin.v1.stats.dependencies import ADMIN_STATS_SERVICE_DEP

from src.presentation.api.v1.schemas import SuccessResponseSchema
from src.presentation.api.admin.v1.stats.schemas import (
    AdminStatsResponse,
    AdminWeeklySalesSchema,
    AdminRecentSalesDetailsSchema,
)

admin_stats = APIRouter(prefix="/stats", tags=["Stats"])


@admin_stats.get("/")
async def get_stats(
    service: ADMIN_STATS_SERVICE_DEP, _current_user: CURRENT_ADMIN_USER_DEP
) -> SuccessResponseSchema[AdminStatsResponse]:
    stats = await service.get_system_stats()
    return SuccessResponseSchema[AdminStatsResponse](
        data=AdminStatsResponse(
            total_users=stats["total_users"],
            total_partners=stats["total_partners"],
            monthly_sales=stats["monthly_sales"],
            products_types_count=stats["product_types_count"],
            weekly_sales=[
                AdminWeeklySalesSchema(**weekly_sale) for weekly_sale in stats["weekly_sales"]
            ],
            recent_sales_details=[
                AdminRecentSalesDetailsSchema(**recent_sales_detail)
                for recent_sales_detail in stats["recent_sales_details"]
            ],
        ),
        message="Stats fetched successfully",
    )
