import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"

import { getPrices } from "../api/prices"
import type { Price } from "../types/api"

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts"

function TickerPage() {
  const { symbol } = useParams()
  const [prices, setPrices] = useState<Price[]>([])
  const [loading, setLoading] = useState(true)

  const chartData = prices
    .slice()
    .reverse()
    .filter((price) => price.close != null)
    .map((price) => ({
      date: price.date,
      close: price.close,
    }))

  async function loadPrices(symbol: string) {
    setLoading(true)

    try {
      const data = await getPrices(symbol)
      setPrices(data)
    } finally {
      setLoading(false)
    }
  }
  
  useEffect(() => {
    if (!symbol) return
    loadPrices(symbol)
  }, [symbol])

  if (loading) return <p>Loading prices...</p>

  if (!loading && prices.length === 0) {
    return <p>No price data available</p>
  }

  return (
    <div>
      <h2>Ticker: {symbol}</h2>
      
      <LineChart width={700} height={300} data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="close" dot={false} />
      </LineChart>
    </div>
  )
}

export default TickerPage