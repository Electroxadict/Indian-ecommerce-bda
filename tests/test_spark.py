import pytest
from spark.rfm_analysis import run_rfm_analysis, assign_rfm_segment
from spark.sales_analytics import get_daily_sales_trend

def test_rfm_scoring_logic():
    segment = assign_rfm_segment(5, 5, 5)
    assert segment == "Champions"
    
    segment_lost = assign_rfm_segment(1, 1, 1)
    assert segment_lost == "Lost / Low Value"

def test_rfm_analysis_execution():
    rfm_df = run_rfm_analysis()
    assert not rfm_df.empty
    assert "segment" in rfm_df.columns
    assert "r_score" in rfm_df.columns

def test_sales_trend_query():
    df_trend = get_daily_sales_trend()
    assert not df_trend.empty
    assert "total_revenue" in df_trend.columns
