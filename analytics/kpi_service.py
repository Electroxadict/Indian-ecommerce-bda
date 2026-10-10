"""
KPI Service computing executive summary metrics.
"""

from utils.db_connector import DBConnector
from utils.logger import get_logger

logger = get_logger("KPIService")

def get_executive_kpis() -> dict:
    """Calculate key executive summary metrics."""
    rev_query = """
    SELECT 
        SUM(total_amount) as total_revenue,
        COUNT(order_id) as total_orders,
        COUNT(DISTINCT customer_id) as active_customers,
        AVG(total_amount) as avg_order_value
    FROM orders
    """
    df = DBConnector.execute_duckdb_query(rev_query)
    if df.empty:
        df = DBConnector.execute_sqlite_query(rev_query)

    prod_query = "SELECT COUNT(*) as total_products FROM products"
    df_prod = DBConnector.execute_duckdb_query(prod_query)

    if not df.empty and df["total_revenue"].values[0] is not None:
        total_revenue = float(df["total_revenue"].values[0])
        total_orders = int(df["total_orders"].values[0])
        active_customers = int(df["active_customers"].values[0])
        aov = float(df["avg_order_value"].values[0])
    else:
        total_revenue, total_orders, active_customers, aov = 0.0, 0, 0, 0.0

    total_products = int(df_prod["total_products"].values[0]) if not df_prod.empty else 0

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "active_customers": active_customers,
        "avg_order_value": round(aov, 2),
        "total_products": total_products
    }
