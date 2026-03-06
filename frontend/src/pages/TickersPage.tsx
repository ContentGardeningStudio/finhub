import { Link } from "react-router-dom"
import { useEffect, useState } from "react"
import { getTickers } from "../api/tickers"
import type { Ticker } from "../types/api"

// const tickers: Ticker[] = [
//  { id: 1, symbol: "AAPL", name: "Apple" },
//  { id: 2, symbol: "MSFT", name: "Microsoft" },
//  { id: 3, symbol: "GOOGL", name: "Alphabet" },
// ]


function TickersPage() {
  const [tickers, setTickers] = useState<Ticker[]>([])

  useEffect(() => {
    getTickers().then(setTickers)
  }, [])

  return (
    <div>
      <h2>Tickers</h2>

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