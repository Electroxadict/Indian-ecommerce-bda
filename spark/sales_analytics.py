"""
PySpark & DuckDB Sales Analytics and Revenue Aggregation Engine.
"""

import pandas as pd
from config.settings import DATA_DIR
from spark.spark_session import get_spark_session
from utils.db_connector import DBConnector
from utils.logger import get_logger

logger = get_logger("SalesAnalytics")

def get_daily_sales_trend() -> pd.DataFrame:
    """Fetch or compute daily sales revenue and order counts."""
    query = """
    SELECT 
        DATE(order_date) as date,
        COUNT(order_id) as total_orders,
        SUM(total_amount) as total_revenue,
        ROUND(AVG(total_amount), 2) as avg_order_value
    FROM orders
    GROUP BY DATE(order_date)
    ORDER BY date ASC
    """
    df = DBConnector.execute_duckdb_query(query)
    if df.empty:
        df = DBConnector.execute_sqlite_query(query)
    return df

def get_category_sales_performance() -> pd.DataFrame:
    """Fetch sales performance grouped by product category."""
    query = """
    SELECT 
        p.category,
        COUNT(DISTINCT oi.order_id) as total_orders,
        SUM(oi.quantity) as total_units_sold,
        ROUND(SUM(oi.total_price), 2) as category_revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category
    ORDER BY category_revenue DESC
    """
    df = DBConnector.execute_duckdb_query(query)
    if df.empty:
        df = DBConnector.execute_sqlite_query(query)
    return df

def get_payment_method_breakdown() -> pd.DataFrame:
    """Fetch breakdown of transactions by payment method."""
    query = """
    SELECT 
        payment_method,
        COUNT(order_id) as transaction_count,
        ROUND(SUM(total_amount), 2) as total_amount
    FROM orders
    GROUP BY payment_method
    ORDER BY total_amount DESC
    """
    df = DBConnector.execute_duckdb_query(query)
    if df.empty:
        df = DBConnector.execute_sqlite_query(query)
    return df
