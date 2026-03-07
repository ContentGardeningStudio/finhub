import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"

import { getPrices } from "../api/prices"
import type { Price } from "../types/api"

function TickerPage() {
  const { symbol } = useParams()
  const [prices, setPrices] = useState<Price[]>([])
  
  async function loadPrices(symbol: string) {
    const data = await getPrices(symbol)
    setPrices(data)
  }
  
  useEffect(() => {
    if (!symbol) return
    loadPrices(symbol)
  }, [symbol])

  return (
    <div>
      <h2>Ticker: {symbol}</h2>
      <ul>
        {prices.map((price) => (
          <li key={price.date}>
            {price.date} — {price.close}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default TickerPage