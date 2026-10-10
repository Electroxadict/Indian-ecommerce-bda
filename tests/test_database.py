import pytest
from utils.db_connector import DBConnector

def test_sqlite_query():
    df = DBConnector.execute_sqlite_query("SELECT 1 as test_val")
    assert not df.empty
    assert df["test_val"].values[0] == 1

def test_duckdb_query():
    df = DBConnector.execute_duckdb_query("SELECT 1 as test_val")
    assert not df.empty
    assert df["test_val"].values[0] == 1

def test_database_tables_exist():
    df = DBConnector.execute_duckdb_query("SHOW TABLES")
    assert not df.empty
    tables = df["name"].tolist() if "name" in df.columns else []
    assert "orders" in tables
    assert "customers" in tables
