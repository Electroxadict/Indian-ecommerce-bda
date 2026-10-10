"""
Centralized Indian Rupee (INR / ₹) Currency Formatting Utility.
Provides standard Indian numbering format (e.g. ₹1,00,000.00) and compact formats (e.g. ₹62.32L).
"""

def format_inr(value: float, include_symbol: bool = True, decimals: int = 2) -> str:
    """
    Formats a numeric value into standard Indian Numbering system format.
    Example:
    1000 -> ₹1,000.00
    100000 -> ₹1,00,000.00
    6231930.50 -> ₹62,31,930.50
    """
    if value is None:
        return "₹0.00" if include_symbol else "0.00"

    try:
        val = float(value)
    except (ValueError, TypeError):
        return "₹0.00" if include_symbol else "0.00"

    is_negative = val < 0
    val = abs(val)

    if decimals > 0:
        fmt_str = f"%.{decimals}f"
        val_str = fmt_str % val
        parts = val_str.split(".")
        int_part = parts[0]
        dec_part = "." + parts[1]
    else:
        int_part = str(int(round(val)))
        dec_part = ""

    if len(int_part) <= 3:
        formatted_int = int_part
    else:
        last_three = int_part[-3:]
        remaining = int_part[:-3]
        # Group in pairs of 2 from right to left
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted_int = ",".join(groups) + "," + last_three

    prefix = "₹" if include_symbol else ""
    sign = "-" if is_negative else ""
    return f"{sign}{prefix}{formatted_int}{dec_part}"


def format_inr_compact(value: float, include_symbol: bool = True) -> str:
    """
    Formats a numeric value into compact Indian notation (Cr, L, K).
    Example:
    6231930 -> ₹62.32L
    12540800 -> ₹1.25Cr
    2077.31 -> ₹2.08K
    """
    if value is None:
        return "₹0" if include_symbol else "0"

    try:
        val = float(value)
    except (ValueError, TypeError):
        return "₹0" if include_symbol else "0"

    is_negative = val < 0
    val = abs(val)
    prefix = "₹" if include_symbol else ""
    sign = "-" if is_negative else ""

    if val >= 1_00_00_000:  # 1 Crore = 10,000,000
        formatted = f"{val / 1_00_00_000:.2f}Cr"
    elif val >= 1_00_000:    # 1 Lakh = 100,000
        formatted = f"{val / 1_00_000:.2f}L"
    elif val >= 1_000:       # 1 Thousand
        formatted = f"{val / 1_000:.2f}K"
    else:
        formatted = f"{val:.2f}"

    return f"{sign}{prefix}{formatted}"
