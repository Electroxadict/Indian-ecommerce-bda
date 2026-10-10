"""
Web Clickstream Funnel Analysis Module.
"""

import pandas as pd
from utils.db_connector import DBConnector
from utils.logger import get_logger

logger = get_logger("FunnelAnalysis")

FUNNEL_STAGES = [
    ("page_view", "Page Views"),
    ("product_view", "Product Views"),
    ("add_to_cart", "Add To Cart"),
    ("checkout_start", "Checkout Started"),
    ("purchase_complete", "Purchase Completed")
]

def get_conversion_funnel() -> pd.DataFrame:
    """Calculates user counts at each stage of the conversion funnel."""
    query = """
    SELECT 
        event_type,
        COUNT(DISTINCT session_id) as unique_sessions,
        COUNT(DISTINCT customer_id) as unique_users,
        COUNT(event_id) as total_events
    FROM web_clickstream
    GROUP BY event_type
    """
    df = DBConnector.execute_duckdb_query(query)
    if df.empty:
        df = DBConnector.execute_sqlite_query(query)
        
    if df.empty:
        return pd.DataFrame()

    funnel_data = []
    prev_users = None

    for event_code, stage_name in FUNNEL_STAGES:
        match = df[df["event_type"] == event_code]
        if not match.empty:
            users = int(match["unique_users"].values[0])
            sessions = int(match["unique_sessions"].values[0])
            events = int(match["total_events"].values[0])
        else:
            users, sessions, events = 0, 0, 0

        conversion_pct = round((users / prev_users * 100), 2) if (prev_users and prev_users > 0) else 100.0
        prev_users = users if users > 0 else prev_users

        funnel_data.append({
            "stage_code": event_code,
            "stage_name": stage_name,
            "unique_users": users,
            "unique_sessions": sessions,
            "total_events": events,
            "conversion_rate_pct": conversion_pct
        })

    return pd.DataFrame(funnel_data)
