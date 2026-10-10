import streamlit as st
from analytics.sales_service import get_sales_trend_chart, get_category_performance_chart, get_payment_method_chart
from analytics.kpi_service import get_executive_kpis
from utils.currency import format_inr

st.set_page_config(page_title="Sales Analytics | Ecommerce-BDA", page_icon="📊", layout="wide")

st.title("📊 Sales & Revenue Analytics (₹)")
st.markdown("Detailed breakdown of revenue trends, product category sales, and payment channel distribution in Indian Rupees (₹).")

kpis = get_executive_kpis()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", format_inr(kpis['total_revenue']))
c2.metric("Total Orders", f"{kpis['total_orders']:,}")
c3.metric("Avg Order Value (AOV)", format_inr(kpis['avg_order_value']))
c4.metric("Active Customers", f"{kpis['active_customers']:,}")

st.divider()

col_left, col_right = st.columns([2, 1])

with col_left:
    fig_trend = get_sales_trend_chart()
    if fig_trend:
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No sales trend data available.")

with col_right:
    fig_payment = get_payment_method_chart()
    if fig_payment:
        st.plotly_chart(fig_payment, use_container_width=True)
    else:
        st.info("No payment method data available.")

st.divider()

fig_category = get_category_performance_chart()
if fig_category:
    st.plotly_chart(fig_category, use_container_width=True)
