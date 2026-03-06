import { Link } from "react-router-dom"
import { useEffect, useState } from "react"
import { getTickers } from "../api/tickers"
import CreateTickerForm from "../components/CreateTickerForm"

import type { Ticker } from "../types/api"


function TickersPage() {
  const [tickers, setTickers] = useState<Ticker[]>([])

  async function loadTickers() {
    const data = await getTickers()
    setTickers(data)
  }

  useEffect(() => {
    loadTickers()
  }, [])

  return (
    <div>
      <h2>Tickers</h2>

      <div>
        <CreateTickerForm onCreated={loadTickers} />
      </div>

      <ul>
        {tickers.map((ticker) => (
          <li key={ticker.id}>
            <Link to={`/tickers/${ticker.symbol}`}>
              {ticker.symbol}
            </Link>{" "}
            — {ticker.name}
          </li>
        ))}
      </ul>

    </div>
  )
}

export default TickersPage
