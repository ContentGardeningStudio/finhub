import { useParams } from "react-router-dom"

function TickerPage() {
  const { symbol } = useParams()

  return (
    <div>
      <h2>Ticker: {symbol}</h2>
    </div>
  )
}

export default TickerPage