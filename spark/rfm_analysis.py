"""
PySpark & DuckDB RFM (Recency, Frequency, Monetary) Customer Segmentation Analysis.
"""

from datetime import datetime
import pandas as pd
import numpy as np
from config.settings import DATA_DIR
from spark.spark_session import get_spark_session
from utils.db_connector import DBConnector
from utils.logger import get_logger

logger = get_logger("RFMAnalysis")

def assign_rfm_segment(r_score: int, f_score: int, m_score: int) -> str:
    rfm_score = r_score * 100 + f_score * 10 + m_score
    if r_score >= 4 and f_score >= 4 and m_score >= 4:
        return "Champions"
    elif r_score >= 3 and f_score >= 3 and m_score >= 3:
        return "Loyal Customers"
    elif r_score >= 3 and f_score <= 2 and m_score >= 3:
        return "Potential Loyalists"
    elif r_score >= 4 and f_score <= 1:
        return "New Customers"
    elif r_score == 3 and f_score == 1:
        return "Promising"
    elif r_score == 2 and f_score >= 3:
        return "At Risk"
    elif r_score <= 2 and f_score >= 4 and m_score >= 4:
        return "Can't Lose Them"
    elif r_score == 2 and f_score <= 2:
        return "Hibernating"
    else:
        return "Lost / Low Value"

def run_rfm_analysis() -> pd.DataFrame:
    """Run RFM segmentation using PySpark or DuckDB fallback."""
    logger.info("Starting RFM Customer Segmentation Job...")
    spark = get_spark_session()

    if spark is not None:
        try:
            logger.info("Executing RFM computation via PySpark...")
            from pyspark.sql import functions as F
            from pyspark.sql.window import Window

            orders_path = str(DATA_DIR / "orders.csv")
            df_orders = spark.read.option("header", "true").option("inferSchema", "true").csv(orders_path)

            # Max date for recency anchor
            max_date = df_orders.select(F.max("order_date")).collect()[0][0]
            if isinstance(max_date, str):
                max_date = datetime.strptime(max_date, "%Y-%m-%d %H:%M:%S")

            rfm_spark = df_orders.groupBy("customer_id").agg(
                F.datediff(F.lit(max_date), F.max("order_date")).alias("recency"),
                F.countDistinct("order_id").alias("frequency"),
                F.round(F.sum("total_amount"), 2).alias("monetary")
            )

            # Compute percentiles for scoring 1-5
            rfm_pd = rfm_spark.toPandas()
            rfm_pd["r_score"] = pd.qcut(rfm_pd["recency"].rank(method="first", ascending=False), 5, labels=[1, 2, 3, 4, 5]).astype(int)
            rfm_pd["f_score"] = pd.qcut(rfm_pd["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
            rfm_pd["m_score"] = pd.qcut(rfm_pd["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
            rfm_pd["rfm_cell"] = rfm_pd["r_score"].astype(str) + rfm_pd["f_score"].astype(str) + rfm_pd["m_score"].astype(str)
            rfm_pd["segment"] = rfm_pd.apply(lambda row: assign_rfm_segment(row["r_score"], row["f_score"], row["m_score"]), axis=1)
            rfm_pd["calculated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save to Database
            DBConnector.save_df_to_sqlite(rfm_pd, "rfm_segments")
            logger.info(f"PySpark RFM Analysis completed. Processed {len(rfm_pd)} customers.")
            return rfm_pd
        except Exception as e:
            logger.error(f"PySpark RFM job error: {e}. Falling back to DuckDB/Pandas.")

    # DuckDB / Pandas Fallback
    logger.info("Executing RFM computation via DuckDB/Pandas...")
    orders_df = pd.read_csv(DATA_DIR / "orders.csv")
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
    max_date = orders_df["order_date"].max()

    rfm_df = orders_df.groupby("customer_id").agg(
        recency=("order_date", lambda x: (max_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("total_amount", "sum")
    ).reset_index()

    rfm_df["r_score"] = pd.qcut(rfm_df["recency"].rank(method="first", ascending=False), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm_df["f_score"] = pd.qcut(rfm_df["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm_df["m_score"] = pd.qcut(rfm_df["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm_df["rfm_cell"] = rfm_df["r_score"].astype(str) + rfm_df["f_score"].astype(str) + rfm_df["m_score"].astype(str)
    rfm_df["segment"] = rfm_df.apply(lambda row: assign_rfm_segment(row["r_score"], row["f_score"], row["m_score"]), axis=1)
    rfm_df["calculated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    DBConnector.save_df_to_sqlite(rfm_df, "rfm_segments")
    logger.info(f"DuckDB/Pandas RFM Analysis completed. Processed {len(rfm_df)} customers.")
    return rfm_df

if __name__ == "__main__":
    run_rfm_analysis()
