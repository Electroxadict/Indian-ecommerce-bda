"""
PySpark Session Manager with fallback handling.
"""

import os
import subprocess
from config.settings import SPARK_APP_NAME, SPARK_MASTER, SPARK_DRIVER_MEMORY
from utils.logger import get_logger

logger = get_logger("SparkSession")

_spark_session = None

def _is_java_compatible() -> bool:
    """Check if installed Java version is compatible with PySpark (Java 17+ for PySpark 4.x)."""
    try:
        res = subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=3)
        output = res.stderr or res.stdout
        # e.g., java version "1.8.0_..." -> 8, or java version "17.0..." -> 17
        if "1.8." in output or "version \"1.8" in output or "version \"1.7" in output:
            logger.warning("Detected legacy Java 8/7. PySpark 4.x requires Java 17+. Utilizing DuckDB/Pandas high-performance engine.")
            return False
        return True
    except Exception:
        return False

def get_spark_session():
    """
    Get or create PySpark session.
    Returns None if PySpark or Java is not installed/configured properly.
    """
    global _spark_session
    if _spark_session is not None:
        return _spark_session

    if not _is_java_compatible():
        return None

    try:
        from pyspark.sql import SparkSession
        logger.info("Initializing PySpark Session...")
        session = SparkSession.builder \
            .appName(SPARK_APP_NAME) \
            .master(SPARK_MASTER) \
            .config("spark.driver.memory", SPARK_DRIVER_MEMORY) \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .config("spark.ui.showConsoleProgress", "false") \
            .getOrCreate()
        
        session.sparkContext.setLogLevel("WARN")
        _spark_session = session
        logger.info("PySpark Session created successfully.")
        return _spark_session
    except Exception as e:
        logger.warning(f"Could not initialize PySpark (falling back to Pandas/DuckDB mode): {e}")
        _spark_session = None
        return None
    except BaseException as e:
        logger.warning(f"PySpark initialization error (falling back to Pandas/DuckDB mode): {e}")
        _spark_session = None
        return None

def stop_spark_session():
    global _spark_session
    if _spark_session is not None:
        try:
            _spark_session.stop()
            _spark_session = None
            logger.info("PySpark Session stopped.")
        except Exception as e:
            logger.error(f"Error stopping PySpark session: {e}")
