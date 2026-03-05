from __future__ import annotations

import datetime as dt
from pydantic import BaseModel, Field


# ---------- Tickers ----------


class TickerCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    name: str | None = Field(default=None, max_length=200)


class TickerOut(BaseModel):
    id: int
    symbol: str
    name: str | None = None

    class Config:
        from_attributes = True


# ---------- Prices ----------


class PriceOut(BaseModel):
    date: dt.date
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = None
    volume: int | None = None

    class Config:
        from_attributes = True


# ---------- Sync ----------


class SyncResult(BaseModel):
    symbol: str
    rows_downloaded: int
    rows_upserted: int
