"""
Product & Inventory Analytics Service in INR (₹).
"""

import pandas as pd
import plotly.express as px
from utils.db_connector import DBConnector
from utils.currency import format_inr
from utils.logger import get_logger

logger = get_logger("ProductService")

def get_top_products(limit: int = 10) -> pd.DataFrame:
    """Fetch top selling products by revenue."""
    query = f"""
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        p.unit_price,
        p.stock_quantity,
        SUM(oi.quantity) as total_units_sold,
        ROUND(SUM(oi.total_price), 2) as total_revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category, p.unit_price, p.stock_quantity
    ORDER BY total_revenue DESC
    LIMIT {limit}
    """
    df = DBConnector.execute_duckdb_query(query)
    if df.empty:
        df = DBConnector.execute_sqlite_query(query)
    return df

def get_low_stock_products(threshold: int = 50) -> pd.DataFrame:
    """Fetch products with inventory below threshold."""
    query = f"""
    SELECT product_id, product_name, category, unit_price, stock_quantity
    FROM products
    WHERE stock_quantity <= {threshold}
    ORDER BY stock_quantity ASC
    """
    df = DBConnector.execute_duckdb_query(query)
    if df.empty:
        df = DBConnector.execute_sqlite_query(query)
    return df

def get_top_products_chart(limit: int = 10):
    """Plotly horizontal bar chart of top selling products in INR (₹)."""
    df = get_top_products(limit)
    if df.empty:
        return None

    df["formatted_revenue"] = df["total_revenue"].apply(lambda x: format_inr(x))

    fig = px.bar(
        df,
        x="total_revenue",
        y="product_name",
        orientation="h",
        color="category",
        title=f"Top {limit} Products by Generated Revenue (₹)",
        labels={"total_revenue": "Revenue (₹)", "product_name": "Product Name"},
        hover_data={"formatted_revenue": True, "total_revenue": False}
    )
    fig.update_traces(hovertemplate="<b>Product</b>: %{y}<br><b>Revenue</b>: %{customdata[0]}<extra></extra>")
    fig.update_layout(
        template="plotly_white",
        yaxis={'categoryorder':'total ascending'},
        xaxis_tickprefix="₹"
    )
    return fig
