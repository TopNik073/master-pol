from pydantic import BaseModel
from datetime import datetime


class AdminWeeklySalesSchema(BaseModel):
    date: datetime
    amount: float


class AdminRecentSalesDetailsSchema(BaseModel):
    date: datetime
    partner_type: str
    partner_name: str
    product_name: str
    amount: float


class AdminStatsResponse(BaseModel):
    total_users: int
    total_partners: int
    monthly_sales: float
    products_types_count: int
    weekly_sales: list[AdminWeeklySalesSchema]
    recent_sales_details: list[AdminRecentSalesDetailsSchema]
