"""
ETL Pipeline script for reading raw e-commerce data, validating, cleaning,
and loading into relational and columnar analytical databases (SQLite & DuckDB).
"""

import pandas as pd
from pathlib import Path
from config.settings import DATA_DIR
from utils.db_connector import DBConnector
from database.db_init import initialize_databases
from ingestion.generator import generate_all_datasets
from utils.logger import get_logger

logger = get_logger("ETLPipeline")

def run_etl_pipeline():
    logger.info("Starting ETL Pipeline Execution...")

    # Step 1: Initialize Database Schemas
    initialize_databases()

    # Step 2: Check or Generate Raw CSV files
    cust_file = DATA_DIR / "customers.csv"
    if not cust_file.exists():
        logger.info("Raw datasets not found. Generating synthetic data...")
        generate_all_datasets(DATA_DIR)

    # Step 3: Read and Clean Datasets
    logger.info("Reading raw CSV files...")
    cust_df = pd.read_csv(DATA_DIR / "customers.csv")
    prod_df = pd.read_csv(DATA_DIR / "products.csv")
    orders_df = pd.read_csv(DATA_DIR / "orders.csv")
    items_df = pd.read_csv(DATA_DIR / "order_items.csv")
    clicks_df = pd.read_csv(DATA_DIR / "web_clickstream.csv")

    # Data Cleaning & Type Casting
    cust_df["signup_date"] = pd.to_datetime(cust_df["signup_date"]).dt.strftime("%Y-%m-%d")
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    clicks_df["event_timestamp"] = pd.to_datetime(clicks_df["event_timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")

    # Step 4: Load into SQLite
    logger.info("Loading cleaned datasets into SQLite...")
    DBConnector.save_df_to_sqlite(cust_df, "customers")
    DBConnector.save_df_to_sqlite(prod_df, "products")
    DBConnector.save_df_to_sqlite(orders_df, "orders")
    DBConnector.save_df_to_sqlite(items_df, "order_items")
    DBConnector.save_df_to_sqlite(clicks_df, "web_clickstream")

    # Step 5: Sync CSVs to DuckDB for ultra-fast columnar analytical queries
    logger.info("Syncing CSV datasets to DuckDB...")
    DBConnector.sync_csvs_to_duckdb(DATA_DIR)

    logger.info("ETL Pipeline completed successfully!")
    return True

if __name__ == "__main__":
    run_etl_pipeline()
