import pytest
import pandas as pd
from config.settings import DATA_DIR
from ingestion.generator import generate_customers, generate_products, generate_orders_and_items, generate_clickstream

def test_data_generation_shapes():
    cust_df = generate_customers(num_customers=50)
    prod_df = generate_products(num_products=20)
    orders_df, items_df = generate_orders_and_items(cust_df, prod_df, num_orders=100)
    clicks_df = generate_clickstream(cust_df, num_events=200)

    assert len(cust_df) == 50
    assert len(prod_df) == 20
    assert len(orders_df) == 100
    assert len(items_df) >= 100
    assert len(clicks_df) == 200

def test_customer_columns():
    cust_df = generate_customers(num_customers=10)
    expected_cols = {"customer_id", "name", "email", "country", "signup_date", "customer_segment"}
    assert expected_cols.issubset(set(cust_df.columns))
