"""
Indian E-Commerce Big Data Analytics Platform - Main Streamlit Entry Point
"""

import streamlit as st
from analytics.kpi_service import get_executive_kpis
from spark.sales_analytics import get_daily_sales_trend
from utils.currency import format_inr, format_inr_compact
import plotly.express as px

st.set_page_config(
    page_title="Indian E-Commerce BDA Platform",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

st.title("🛒 Indian E-Commerce Big Data Analytics Platform")
st.markdown("""
An enterprise Big Data Analytics suite for the Indian marketplace featuring synthetic data generation in INR (₹),
ETL loading into DuckDB & SQLite, PySpark batch analytics (RFM segmentation & sales aggregations), and an interactive multi-page dashboard.
""")

st.divider()

# High-Level KPIs formatted in INR (₹)
kpis = get_executive_kpis()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("💰 Total Revenue", format_inr(kpis['total_revenue']))
kpi2.metric("📦 Total Orders", f"{kpis['total_orders']:,}")
kpi3.metric("👤 Active Customers", f"{kpis['active_customers']:,}")
kpi4.metric("📈 Avg Order Value", format_inr(kpis['avg_order_value']))
kpi5.metric("🛍️ Total Products", f"{kpis['total_products']:,}")

st.divider()

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 Daily Revenue Performance (₹)")
    df_trend = get_daily_sales_trend()
    if not df_trend.empty:
        df_trend["formatted_revenue"] = df_trend["total_revenue"].apply(lambda x: format_inr(x))
        fig = px.area(
            df_trend,
            x="date",
            y="total_revenue",
            title="Revenue Over Time (₹)",
            labels={"date": "Date", "total_revenue": "Revenue (₹)"},
            hover_data={"formatted_revenue": True, "total_revenue": False}
        )
        fig.update_traces(hovertemplate="<b>Date</b>: %{x}<br><b>Revenue</b>: %{customdata[0]}<extra></extra>")
        fig.update_layout(
            template="plotly_white",
            yaxis_tickprefix="₹"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data found. Please run the ETL Pipeline on the 'Data Pipeline & Spark' page.")

with col_right:
    st.subheader("🧭 Platform Navigation")
    st.markdown("""
    Select a module from the left sidebar:

    - **📊 Sales Analytics**: Track daily revenue, payment methods (UPI, Cards, COD), and category sales in ₹.
    - **👤 Customer Insights**: Explore RFM customer segmentation matrix and Indian geographic distribution.
    - **📦 Product Performance**: Identify top seller products and low stock inventory alerts in ₹.
    - **⚡ Data Pipeline & Spark**: Trigger ETL jobs, PySpark batch pipelines, and clickstream conversion funnels.
    - **🔍 SQL Workbench**: Run ad-hoc SQL queries on DuckDB and SQLite databases.
    """)

st.info("💡 **System Status**: SQLite & DuckDB analytical engines online in INR mode. Navigation menu ready.")
