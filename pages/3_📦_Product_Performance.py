import streamlit as st
from analytics.product_service import get_top_products_chart, get_top_products, get_low_stock_products
from utils.currency import format_inr

st.set_page_config(page_title="Product Performance | Ecommerce-BDA", page_icon="📦", layout="wide")

st.title("📦 Product & Inventory Performance (₹)")
st.markdown("Track top-selling items, revenue generation per product in Indian Rupees (₹), and monitor low inventory stock levels.")

col1, col2 = st.columns([2, 1])

with col1:
    fig_top = get_top_products_chart(limit=10)
    if fig_top:
        st.plotly_chart(fig_top, use_container_width=True)

with col2:
    st.subheader("⚠️ Low Stock Alert")
    threshold = st.slider("Stock Quantity Threshold", min_value=10, max_value=100, value=50)
    df_low_stock = get_low_stock_products(threshold=threshold)
    if not df_low_stock.empty:
        df_low_stock["unit_price_formatted"] = df_low_stock["unit_price"].apply(lambda x: format_inr(x))
    st.dataframe(df_low_stock, use_container_width=True)

st.divider()
st.subheader("Top Product Sales Leaderboard (₹)")
df_top = get_top_products(20)
if not df_top.empty:
    df_top["unit_price_formatted"] = df_top["unit_price"].apply(lambda x: format_inr(x))
    df_top["total_revenue_formatted"] = df_top["total_revenue"].apply(lambda x: format_inr(x))
st.dataframe(df_top, use_container_width=True)
