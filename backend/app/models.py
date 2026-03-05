from __future__ import annotations

import datetime as dt
from sqlalchemy import (
    String,
    Integer,
    Date,
    Float,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


class Ticker(Base):
    __tablename__ = "tickers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)

    prices: Mapped[list["Price"]] = relationship(
        back_populates="ticker",
        cascade="all, delete-orphan",
    )


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker_id: Mapped[int] = mapped_column(
        ForeignKey("tickers.id", ondelete="CASCADE"), index=True
    )

    date: Mapped[dt.date] = mapped_column(Date, index=True)

    open: Mapped[float | None] = mapped_column(Float, nullable=True)
    high: Mapped[float | None] = mapped_column(Float, nullable=True)
    low: Mapped[float | None] = mapped_column(Float, nullable=True)
    close: Mapped[float | None] = mapped_column(Float, nullable=True)
    volume: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    ticker: Mapped["Ticker"] = relationship(back_populates="prices")

    __table_args__ = (
        UniqueConstraint("ticker_id", "date", name="uq_prices_ticker_date"),
        Index("ix_prices_ticker_date", "ticker_id", "date"),
    )
