"""
Configuration settings for the E-Commerce BDA Platform.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv(dotenv_path=BASE_DIR / ".env.example")

# App Configuration
APP_NAME = os.getenv("APP_NAME", "E-Commerce Big Data Analytics Platform")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

# Directory Paths
DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")
DATABASE_DIR = BASE_DIR / "database"
ASSETS_DIR = BASE_DIR / "assets"

# Database Paths
SQLITE_DB_PATH = DATABASE_DIR / "ecommerce.db"
DUCKDB_PATH = DATABASE_DIR / "ecommerce.duckdb"

# Spark Settings
SPARK_APP_NAME = os.getenv("SPARK_APP_NAME", "EcommerceAnalyticsSpark")
SPARK_MASTER = os.getenv("SPARK_MASTER", "local[*]")
SPARK_DRIVER_MEMORY = os.getenv("SPARK_DRIVER_MEMORY", "2g")

# Ensure required directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
