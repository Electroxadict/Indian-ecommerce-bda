import pytest
from utils.currency import format_inr, format_inr_compact

def test_format_inr_basic():
    assert format_inr(1000) == "₹1,000.00"
    assert format_inr(100000) == "₹1,00,000.00"
    assert format_inr(6231930.50) == "₹62,31,930.50"
    assert format_inr(12540800.75) == "₹1,25,40,800.75"

def test_format_inr_no_symbol():
    assert format_inr(100000, include_symbol=False) == "1,00,000.00"

def test_format_inr_compact():
    assert format_inr_compact(6231930) == "₹62.32L"
    assert format_inr_compact(12540800) == "₹1.25Cr"
    assert format_inr_compact(2500) == "₹2.50K"
    assert format_inr_compact(500) == "₹500.00"
