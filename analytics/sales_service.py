"""
Sales Analytics service for generating charts and sales performance views in INR (₹).
"""

import pandas as pd
import plotly.express as px
from spark.sales_analytics import get_daily_sales_trend, get_category_sales_performance, get_payment_method_breakdown
from utils.currency import format_inr
from utils.logger import get_logger

logger = get_logger("SalesService")

def get_sales_trend_chart():
    """Build Plotly Line Chart for Daily Revenue in INR (₹)."""
    df = get_daily_sales_trend()
    if df.empty:
        return None

    df["date"] = pd.to_datetime(df["date"])
    df["formatted_revenue"] = df["total_revenue"].apply(lambda x: format_inr(x))

    fig = px.line(
        df,
        x="date",
        y="total_revenue",
        title="Daily Sales Revenue Trend (₹)",
        labels={"date": "Date", "total_revenue": "Revenue (₹)"},
        hover_data={"formatted_revenue": True, "total_revenue": False},
        markers=True
    )
    fig.update_traces(hovertemplate="<b>Date</b>: %{x}<br><b>Revenue</b>: %{customdata[0]}<extra></extra>")
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        yaxis_tickprefix="₹"
    )
    return fig

def get_category_performance_chart():
    """Build Plotly Bar Chart for Sales by Product Category in INR (₹)."""
    df = get_category_sales_performance()
    if df.empty:
        return None

    df["formatted_revenue"] = df["category_revenue"].apply(lambda x: format_inr(x))

    fig = px.bar(
        df,
        x="category",
        y="category_revenue",
        color="category",
        title="Revenue by Product Category (₹)",
        labels={"category": "Product Category", "category_revenue": "Revenue (₹)"},
        hover_data={"formatted_revenue": True, "category_revenue": False}
    )
    fig.update_traces(hovertemplate="<b>Category</b>: %{x}<br><b>Revenue</b>: %{customdata[0]}<extra></extra>")
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        yaxis_tickprefix="₹"
    )
    return fig

def get_payment_method_chart():
    """Build Plotly Donut Chart for Payment Method Distribution in INR (₹)."""
    df = get_payment_method_breakdown()
    if df.empty:
        return None

    df["formatted_amount"] = df["total_amount"].apply(lambda x: format_inr(x))

    fig = px.pie(
        df,
        names="payment_method",
        values="total_amount",
        title="Revenue Distribution by Payment Method (₹)",
        hole=0.4,
        hover_data={"formatted_amount": True, "total_amount": False}
    )
    fig.update_traces(hovertemplate="<b>Payment Method</b>: %{label}<br><b>Total Revenue</b>: %{customdata[0]}<extra></extra>")
    fig.update_layout(template="plotly_white")
    return fig
