from __future__ import annotations

import datetime as dt
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .settings import settings
from .db import Base, engine, get_db
from . import crud, schemas
from .yf_service import download_daily_ohlcv

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}


@app.get("/tickers", response_model=list[schemas.TickerOut])
def list_tickers(db: Session = Depends(get_db)):
    return crud.list_tickers(db)


@app.post("/tickers", response_model=schemas.TickerOut)
def add_ticker(payload: schemas.TickerCreate, db: Session = Depends(get_db)):
    return crud.create_ticker(db, payload)


@app.post("/tickers/{symbol}/sync", response_model=schemas.SyncResult)
def sync_ticker(
    symbol: str,
    period: str = Query(
        default="1y", description="yfinance period, e.g. 1mo, 6mo, 1y, 5y, max"
    ),
    db: Session = Depends(get_db),
):
    ticker = crud.get_ticker_by_symbol(db, symbol)
    if ticker is None:
        # convenience: auto-create
        ticker = crud.create_ticker(db, schemas.TickerCreate(symbol=symbol))

    df = download_daily_ohlcv(ticker.symbol, period=period)
    if df.empty:
        return schemas.SyncResult(
            symbol=ticker.symbol, rows_downloaded=0, rows_upserted=0
        )

    rows = df.to_dict(orient="records")
    upserted = crud.upsert_prices_for_ticker(db, ticker, rows)

    return schemas.SyncResult(
        symbol=ticker.symbol,
        rows_downloaded=len(rows),
        rows_upserted=upserted,
    )


@app.get("/prices/{symbol}", response_model=list[schemas.PriceOut])
def get_prices(
    symbol: str,
    start: dt.date | None = Query(default=None),
    end: dt.date | None = Query(default=None),
    limit: int = Query(default=500, ge=1, le=5000),
    db: Session = Depends(get_db),
):
    ticker = crud.get_ticker_by_symbol(db, symbol)
    if ticker is None:
        raise HTTPException(status_code=404, detail="Ticker not found")

    return crud.list_prices(db, ticker, start=start, end=end, limit=limit)
