from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.repositories.base_repo import AbstractRepo
from typing import Dict, Any

REPO_T = TypeVar("REPO_T", bound=AbstractRepo)


class AdminStatsService:
    def __init__(self, repo: REPO_T, session: AsyncSession):
        self._repo = repo
        self.session = session

    async def get_system_stats(self) -> dict[str, Any]:
        """
        Get comprehensive system statistics including users, partners, sales, and product information.
        Returns:
            - total_users: int
            - total_partners: int
            - monthly_sales: float
            - product_types_count: int
            - weekly_sales: list[dict] - список продаж по дням недели
            - recent_sales_details: list[dict] - детали последних продаж
        """
        stats_query = """
        WITH 
        metrics AS (
            SELECT 
                (SELECT COUNT(*) FROM users) as total_users,
                (SELECT COUNT(*) FROM partners) as total_partners,
                (SELECT COUNT(*) FROM products_types) as product_types_count
        ),
        
        monthly_sales AS (
            SELECT 
                COALESCE(SUM(p.quantity_products * pi.minimum_cost), 0) as total_monthly_sales
            FROM products p
            JOIN products_import pi ON p.product_import_id = pi.id
            WHERE p.sell_date >= DATE_TRUNC('month', CURRENT_DATE)
        ),
        
        weekly_sales_by_day AS (
            SELECT 
                DATE(p.sell_date) as sale_date,
                SUM(p.quantity_products * pi.minimum_cost) as daily_sales
            FROM products p
            JOIN products_import pi ON p.product_import_id = pi.id
            WHERE p.sell_date >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY DATE(p.sell_date)
            ORDER BY sale_date
        ),
        
        recent_sales AS (
            SELECT 
                p.sell_date,
                pt.partner_type,
                pt.name as partner_name,
                pi.name as product_name,
                p.quantity_products * pi.minimum_cost as sale_amount
            FROM products p
            JOIN products_import pi ON p.product_import_id = pi.id
            JOIN partners pt ON p.partner_id = pt.id
            ORDER BY p.sell_date DESC
            LIMIT 5
        )
        
        SELECT 
            m.total_users,
            m.total_partners,
            ms.total_monthly_sales,
            m.product_types_count,
            (
                SELECT json_agg(
                    json_build_object(
                        'date', ws.sale_date,
                        'amount', ws.daily_sales
                    )
                )
                FROM weekly_sales_by_day ws
            ) as weekly_sales,
            (
                SELECT json_agg(
                    json_build_object(
                        'date', rs.sell_date,
                        'partner_type', rs.partner_type,
                        'partner_name', rs.partner_name,
                        'product_name', rs.product_name,
                        'amount', rs.sale_amount
                    )
                )
                FROM recent_sales rs
            ) as recent_sales_details
        FROM metrics m
        CROSS JOIN monthly_sales ms
        """
        
        result = await self._repo.execute_sql_script(self.session, stats_query)
        if not result:
            return {}
            
        row = result.first()
        if not row:
            return {}
        
        return {
            "total_users": row[0],
            "total_partners": row[1],
            "monthly_sales": float(row[2]),
            "product_types_count": row[3],
            "weekly_sales": row[4] or [],  # Список продаж по дням недели
            "recent_sales_details": row[5] or []  # Детали последних продаж
        }
