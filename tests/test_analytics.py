import pytest
from analytics.kpi_service import get_executive_kpis
from analytics.customer_service import get_rfm_segment_distribution
from analytics.product_service import get_top_products

def test_executive_kpis():
    kpis = get_executive_kpis()
    assert isinstance(kpis, dict)
    assert kpis["total_revenue"] >= 0
    assert kpis["total_orders"] >= 0

def test_rfm_distribution():
    df = get_rfm_segment_distribution()
    assert not df.empty
    assert "segment" in df.columns

def test_top_products():
    df = get_top_products(5)
    assert not df.empty
    assert len(df) <= 5
