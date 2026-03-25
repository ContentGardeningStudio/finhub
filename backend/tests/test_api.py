import pandas as pd
from unittest.mock import patch


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app" in data


def test_tickers_endpoint_returns_list(client):
    response = client.get("/tickers")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_ticker(client):
    response = client.post("/tickers", json={"symbol": "TEST", "name": "Test"})

    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "TEST"
    assert data["name"] == "Test"


def test_create_and_list_ticker(client):
    client.post("/tickers", json={"symbol": "TEST", "name": "Test"})

    response = client.get("/tickers")
    data = response.json()

    assert any(t["symbol"] == "TEST" for t in data)


def test_create_ticker_normalizes_symbol(client):
    response = client.post(
        "/tickers",
        json={"symbol": " aapl ", "name": "Apple"},
    )

    assert response.status_code == 200
    data = response.json()

    # API response should already be normalized
    assert data["symbol"] == "AAPL"

    # Fetch again to ensure DB stored normalized value
    response = client.get("/tickers")
    assert response.status_code == 200

    tickers = response.json()

    assert any(t["symbol"] == "AAPL" for t in tickers)


def test_create_ticker_is_idempotent(client):
    response1 = client.post("/tickers", json={"symbol": "aapl", "name": "Apple"})
    response2 = client.post("/tickers", json={"symbol": " AAPL ", "name": "Apple"})

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    assert data1["id"] == data2["id"]
    assert data1["symbol"] == "AAPL"
    assert data2["symbol"] == "AAPL"


def test_sync_and_get_prices(client):
    fake_df = pd.DataFrame(
        [
            {
                "date": pd.Timestamp("2026-03-04").date(),
                "open": 180.0,
                "high": 184.0,
                "low": 179.5,
                "close": 183.2,
                "volume": 50000000,
            },
            {
                "date": pd.Timestamp("2026-03-05").date(),
                "open": 183.0,
                "high": 185.0,
                "low": 182.0,
                "close": 184.5,
                "volume": 47000000,
            },
        ]
    )

    with patch("app.main.download_daily_ohlcv", return_value=fake_df):
        sync_response = client.post("/tickers/AAPL/sync?period=1mo")

    assert sync_response.status_code == 200
    sync_data = sync_response.json()
    assert sync_data["symbol"] == "AAPL"
    assert sync_data["rows_downloaded"] == 2
    assert sync_data["rows_upserted"] == 2

    prices_response = client.get("/prices/AAPL?limit=10")
    assert prices_response.status_code == 200

    prices_data = prices_response.json()
    assert len(prices_data) == 2

    assert prices_data[0]["date"] == "2026-03-05"
    assert prices_data[0]["close"] == 184.5

    assert prices_data[1]["date"] == "2026-03-04"
    assert prices_data[1]["close"] == 183.2