"""
Database connector module providing SQLite and DuckDB connection management.
"""

import sqlite3
import duckdb
import pandas as pd
from pathlib import Path
from config.settings import SQLITE_DB_PATH, DUCKDB_PATH
from utils.logger import get_logger

logger = get_logger("DBConnector")

class DBConnector:
    @staticmethod
    def get_sqlite_connection():
        """Get SQLite database connection."""
        SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(str(SQLITE_DB_PATH))

    @staticmethod
    def get_duckdb_connection():
        """Get DuckDB database connection."""
        DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
        return duckdb.connect(str(DUCKDB_PATH))

    @classmethod
    def execute_sqlite_query(cls, query: str, params=None) -> pd.DataFrame:
        """Execute SELECT query on SQLite and return Pandas DataFrame."""
        try:
            with cls.get_sqlite_connection() as conn:
                return pd.read_sql_query(query, conn, params=params)
        except Exception as e:
            logger.error(f"SQLite Query Error: {e}")
            return pd.DataFrame()

    @classmethod
    def execute_duckdb_query(cls, query: str) -> pd.DataFrame:
        """Execute SQL query on DuckDB and return Pandas DataFrame."""
        try:
            conn = cls.get_duckdb_connection()
            df = conn.execute(query).df()
            conn.close()
            return df
        except Exception as e:
            logger.error(f"DuckDB Query Error: {e}")
            return pd.DataFrame()

    @classmethod
    def save_df_to_sqlite(cls, df: pd.DataFrame, table_name: str, if_exists: str = "replace"):
        """Save a Pandas DataFrame to SQLite table."""
        try:
            with cls.get_sqlite_connection() as conn:
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            logger.info(f"Saved {len(df)} rows to SQLite table '{table_name}'.")
        except Exception as e:
            logger.error(f"Error saving to SQLite table '{table_name}': {e}")
            raise e

    @classmethod
    def sync_csvs_to_duckdb(cls, data_dir: Path):
        """Register CSV files in data_dir into DuckDB views/tables."""
        try:
            conn = cls.get_duckdb_connection()
            conn.execute("SET preserve_insertion_order = false;")
            for csv_file in data_dir.glob("*.csv"):
                table_name = csv_file.stem
                conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_file.as_posix()}')")
                logger.info(f"DuckDB registered table '{table_name}' from {csv_file.name}")
            conn.close()
        except Exception as e:
            logger.error(f"Error syncing CSVs to DuckDB: {e}")
