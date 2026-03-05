from __future__ import annotations

import math
import datetime as dt
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Ticker, Price
from .schemas import TickerCreate


def list_tickers(db: Session) -> list[Ticker]:
    return list(db.scalars(select(Ticker).order_by(Ticker.symbol)).all())


def get_ticker_by_symbol(db: Session, symbol: str) -> Ticker | None:
    symbol = symbol.upper().strip()
    return db.scalar(select(Ticker).where(Ticker.symbol == symbol))


def create_ticker(db: Session, payload: TickerCreate) -> Ticker:
    symbol = payload.symbol.upper().strip()
    existing = get_ticker_by_symbol(db, symbol)
    if existing:
        return existing
    obj = Ticker(symbol=symbol, name=payload.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def _nan_to_none(x):
    if x is None:
        return None
    try:
        if isinstance(x, float) and math.isnan(x):
            return None
    except Exception:
        pass
    return x


def upsert_prices_for_ticker(
    db: Session,
    ticker: Ticker,
    rows: list[dict],
) -> int:
    """
    rows: [{date, open, high, low, close, volume}, ...]
    Upsert by (ticker_id, date). Returns number of upserted rows.
    """
    upserted = 0

    for r in rows:
        d: dt.date = r["date"]
        # d: dt.date = r.get("date")  # then validate
        # if d is None:
        #     raise ValueError("Row missing 'date' field")

        existing = db.scalar(
            select(Price).where(Price.ticker_id == ticker.id, Price.date == d)
        )

        if existing is None:
            existing = Price(ticker_id=ticker.id, date=d)
            db.add(existing)

        existing.open = _nan_to_none(r.get("open"))
        existing.high = _nan_to_none(r.get("high"))
        existing.low = _nan_to_none(r.get("low"))
        existing.close = _nan_to_none(r.get("close"))
        existing.volume = _nan_to_none(r.get("volume"))

        upserted += 1

    db.commit()
    return upserted


def list_prices(
    db: Session,
    ticker: Ticker,
    *,
    start: dt.date | None = None,
    end: dt.date | None = None,
    limit: int = 500,
) -> list[Price]:
    q = select(Price).where(Price.ticker_id == ticker.id)
    if start:
        q = q.where(Price.date >= start)
    if end:
        q = q.where(Price.date <= end)
    q = q.order_by(Price.date.desc()).limit(limit)
    return list(db.scalars(q).all())
