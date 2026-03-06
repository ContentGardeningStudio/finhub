import { Routes, Route, Link } from "react-router-dom"

import HomePage from "./pages/HomePage"
import TickersPage from "./pages/TickersPage"
import TickerPage from "./pages/TickerPage"

function App() {
  return (
    <div>

      <nav>
        <Link to="/">Home</Link> |{" "}
        <Link to="/tickers">Tickers</Link>
      </nav>

      <Routes>
        <Route path="/" element={<HomePage />} />

        <Route path="/tickers" element={<TickersPage />} />

        <Route path="/tickers/:symbol" element={<TickerPage />} />
      </Routes>

    </div>
  )
}

export default App