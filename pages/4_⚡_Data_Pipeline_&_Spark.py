import streamlit as st
from ingestion.etl_pipeline import run_etl_pipeline
from spark.rfm_analysis import run_rfm_analysis
from spark.funnel_analysis import get_conversion_funnel
import plotly.express as px

st.set_page_config(page_title="Data Pipeline & Spark | Ecommerce-BDA", page_icon="⚡", layout="wide")

st.title("⚡ Data Ingestion, ETL & PySpark Pipeline Controls")
st.markdown("Trigger real-time synthetic data generation for Indian marketplace (₹), database ETL loading, PySpark RFM batch jobs, and conversion funnel analytics.")

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("🚀 Run Full Data Ingestion & ETL Pipeline (INR Dataset)", use_container_width=True):
        with st.spinner("Generating raw Indian marketplace datasets and syncing DuckDB/SQLite..."):
            success = run_etl_pipeline()
            if success:
                st.success("ETL Pipeline completed successfully! SQLite & DuckDB databases updated with INR (₹) datasets.")
            else:
                st.error("ETL Pipeline failed. Check console logs.")

with col_btn2:
    if st.button("🔥 Execute PySpark / DuckDB RFM Analytics Job", use_container_width=True):
        with st.spinner("Processing PySpark customer RFM clustering job..."):
            rfm_df = run_rfm_analysis()
            st.success(f"RFM Analysis complete! Processed {len(rfm_df)} customer profiles in ₹.")

st.divider()

st.subheader("🌐 User Clickstream Conversion Funnel")
df_funnel = get_conversion_funnel()

if not df_funnel.empty:
    fig_funnel = px.funnel(
        df_funnel,
        x="unique_users",
        y="stage_name",
        title="Session Conversion Funnel (Unique Users per Stage)"
    )
    fig_funnel.update_layout(template="plotly_white")
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    st.subheader("Funnel Stage Breakdown")
    st.dataframe(df_funnel, use_container_width=True)
else:
    st.info("No clickstream data available. Click 'Run Full Data Ingestion & ETL Pipeline' to populate data.")
