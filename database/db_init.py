"""
Database initialization script to execute DDL schema statements.
"""

from pathlib import Path
from utils.db_connector import DBConnector
from utils.logger import get_logger

logger = get_logger("DBInit")

def initialize_databases():
    schema_file = Path(__file__).parent / "schema.sql"
    if not schema_file.exists():
        logger.error("schema.sql not found.")
        return False
    
    with open(schema_file, "r") as f:
        sql_script = f.read()

    # Split statements
    statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]

    # Initialize SQLite
    try:
        conn = DBConnector.get_sqlite_connection()
        cursor = conn.cursor()
        for stmt in statements:
            cursor.execute(stmt)
        conn.commit()
        conn.close()
        logger.info("SQLite database tables successfully initialized.")
    except Exception as e:
        logger.error(f"Error initializing SQLite database: {e}")

    # Initialize DuckDB
    try:
        conn = DBConnector.get_duckdb_connection()
        for stmt in statements:
            conn.execute(stmt)
        conn.close()
        logger.info("DuckDB database tables successfully initialized.")
    except Exception as e:
        logger.error(f"Error initializing DuckDB database: {e}")

    return True

if __name__ == "__main__":
    initialize_databases()
