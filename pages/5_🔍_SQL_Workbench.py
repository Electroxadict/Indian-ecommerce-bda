import streamlit as st
from utils.db_connector import DBConnector

st.set_page_config(page_title="SQL Workbench | Ecommerce-BDA", page_icon="🔍", layout="wide")

st.title("🔍 SQL Analytical Workbench")
st.markdown("Execute ad-hoc SQL queries directly against **DuckDB** (ultra-fast columnar engine) or **SQLite** for Indian E-Commerce data.")

db_engine = st.radio("Select Query Engine:", ["DuckDB (Recommended)", "SQLite"], horizontal=True)

default_query = """SELECT p.category, COUNT(o.order_id) as total_orders, ROUND(SUM(o.total_amount), 2) as total_revenue_inr
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue_inr DESC;"""

sql_query = st.text_area("Write SQL Query:", value=default_query, height=150)

if st.button("▶️ Execute Query", type="primary"):
    with st.spinner("Executing SQL query..."):
        if "DuckDB" in db_engine:
            df_result = DBConnector.execute_duckdb_query(sql_query)
        else:
            df_result = DBConnector.execute_sqlite_query(sql_query)

        st.subheader("Query Results")
        st.write(f"Returned {len(df_result)} rows.")
        st.dataframe(df_result, use_container_width=True)

st.sidebar.markdown("### Schema Reference")
st.sidebar.code("""
customers (customer_id, name, email, city, state, country, signup_date, customer_segment)
products (product_id, product_name, category, sub_category, unit_price, cost_price, stock_quantity)
orders (order_id, customer_id, order_date, payment_method, shipping_city, order_status, total_amount)
order_items (item_id, order_id, product_id, quantity, unit_price, discount_amount, total_price)
web_clickstream (event_id, customer_id, session_id, event_type, page_url, event_timestamp)
rfm_segments (customer_id, recency, frequency, monetary, r_score, f_score, m_score, rfm_cell, segment)
""")
