import streamlit as st
from analytics.customer_service import get_rfm_segment_chart, get_rfm_segment_distribution, get_geographic_chart
from utils.db_connector import DBConnector
from utils.currency import format_inr

st.set_page_config(page_title="Customer Insights | Ecommerce-BDA", page_icon="👤", layout="wide")

st.title("👤 Customer Analytics & RFM Segmentation")
st.markdown("Analyze customer lifetime value in INR (₹), RFM behavioral clusters (Recency, Frequency, Monetary), and Indian geographic distribution.")

tab1, tab2, tab3 = st.tabs(["RFM Segmentation", "Demographics & Geo (India)", "Customer Directory"])

with tab1:
    st.subheader("RFM Customer Segmentation Matrix (Spend in ₹)")
    fig_rfm = get_rfm_segment_chart()
    if fig_rfm:
        st.plotly_chart(fig_rfm, use_container_width=True)
    
    st.subheader("Segment Summary Metrics")
    df_rfm_summary = get_rfm_segment_distribution()
    if not df_rfm_summary.empty:
        df_rfm_summary["avg_monetary_formatted"] = df_rfm_summary["avg_monetary"].apply(lambda x: format_inr(x))
    st.dataframe(df_rfm_summary, use_container_width=True)

with tab2:
    st.subheader("Customer Geographic Distribution across Indian Cities")
    fig_geo = get_geographic_chart()
    if fig_geo:
        st.plotly_chart(fig_geo, use_container_width=True)

with tab3:
    st.subheader("Customer Master Directory")
    df_cust = DBConnector.execute_duckdb_query("SELECT * FROM customers LIMIT 100")
    if df_cust.empty:
        df_cust = DBConnector.execute_sqlite_query("SELECT * FROM customers LIMIT 100")
    st.dataframe(df_cust, use_container_width=True)
