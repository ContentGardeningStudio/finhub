from __future__ import annotations

import pandas as pd
import yfinance as yf


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten MultiIndex columns into strings."""
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [
            " ".join([str(x) for x in col if x not in (None, "")]).strip()
            for col in df.columns
        ]
    return df


def _find_col(df: pd.DataFrame, keyword: str, symbol: str) -> str | None:
    """
    Find a column corresponding to a given keyword (Open/High/Low/Close/Volume),
    regardless of whether the column looks like:
      - "Open"
      - "AAPL Open"
      - "Open AAPL"
      - "AAPL  Open" (we normalize whitespace)
    """
    kw = keyword.lower()
    sym = symbol.lower()

    # Normalize a working view of column names
    cols = []
    for c in df.columns:
        s = str(c)
        s_norm = " ".join(s.split())  # collapse whitespace
        cols.append((c, s_norm, s_norm.lower()))

    # 1) Exact match: "Open"
    for orig, norm, low in cols:
        if low == kw:
            return orig

    # 2) Symbol + keyword in any order (and adjacent)
    #    Examples: "AAPL Open", "Open AAPL"
    for orig, norm, low in cols:
        if kw in low and sym in low:
            return orig

    # 3) Keyword present anywhere (fallback)
    for orig, norm, low in cols:
        if kw in low:
            return orig

    return None


def download_daily_ohlcv(symbol: str, *, period: str = "1y") -> pd.DataFrame:
    symbol = symbol.upper().strip()

    df = yf.download(
        tickers=symbol,
        period=period,
        interval="1d",
        auto_adjust=False,
        progress=False,
        group_by="column",
        threads=False,
    )

    if df is None or df.empty:
        return pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])

    df = _flatten_columns(df)

    # Ensure we always have a 'date' column
    df = df.rename_axis("date").reset_index()
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None).dt.date

    mapping = {}
    for src_kw, dst in [
        ("Open", "open"),
        ("High", "high"),
        ("Low", "low"),
        ("Close", "close"),
        ("Volume", "volume"),
    ]:
        col = _find_col(df, src_kw, symbol)
        if col is not None:
            mapping[col] = dst

    out = df[["date"] + list(mapping.keys())].rename(columns=mapping)

    # Ensure all expected columns exist
    for col in ["open", "high", "low", "close", "volume"]:
        if col not in out.columns:
            out[col] = None

    return out
