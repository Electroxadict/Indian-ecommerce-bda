"""
Customer Analytics service for RFM distribution, demographics, and retention insights in INR (₹).
"""

import pandas as pd
import plotly.express as px
from utils.db_connector import DBConnector
from utils.currency import format_inr
from utils.logger import get_logger

logger = get_logger("CustomerService")

def get_rfm_segment_distribution():
    """Fetch count of customers per RFM Segment with average monetary value."""
    query = """
    SELECT segment, COUNT(customer_id) as customer_count, ROUND(AVG(monetary), 2) as avg_monetary
    FROM rfm_segments
    GROUP BY segment
    ORDER BY customer_count DESC
    """
    df = DBConnector.execute_duckdb_query(query)
    if df.empty:
        df = DBConnector.execute_sqlite_query(query)
    return df

def get_rfm_segment_chart():
    """Plotly Treemap for RFM Customer Segments (Values in ₹)."""
    df = get_rfm_segment_distribution()
    if df.empty:
        return None

    df["formatted_avg_monetary"] = df["avg_monetary"].apply(lambda x: format_inr(x))

    fig = px.treemap(
        df,
        path=["segment"],
        values="customer_count",
        color="avg_monetary",
        color_continuous_scale="Viridis",
        title="Customer RFM Segmentation Matrix (Size = Count, Color = Avg Spend in ₹)",
        hover_data={"formatted_avg_monetary": True, "avg_monetary": False}
    )
    fig.update_traces(hovertemplate="<b>Segment</b>: %{label}<br><b>Customers</b>: %{value}<br><b>Avg Spend</b>: %{customdata[0]}<extra></extra>")
    fig.update_layout(template="plotly_white")
    return fig

def get_customer_geographic_distribution():
    """Fetch count of customers by Indian City."""
    query = """
    SELECT city, state, COUNT(customer_id) as customer_count
    FROM customers
    GROUP BY city, state
    ORDER BY customer_count DESC
    """
    df = DBConnector.execute_duckdb_query(query)
    if df.empty:
        df = DBConnector.execute_sqlite_query(query)
    return df

def get_geographic_chart():
    """Plotly Bar chart of customer city/state breakdown in India."""
    df = get_customer_geographic_distribution()
    if df.empty:
        return None

    fig = px.bar(
        df,
        x="city",
        y="customer_count",
        color="state",
        title="Customer Geographic Breakdown (Indian Cities)",
        labels={"city": "City", "customer_count": "Customers", "state": "State"}
    )
    fig.update_layout(template="plotly_white")
    return fig
