import { apiFetch } from "./client"
import type { Ticker } from "../types/api"
// import type { SyncResult } from "../types/api"

export function getTickers() {
  return apiFetch<Ticker[]>("/tickers")
}