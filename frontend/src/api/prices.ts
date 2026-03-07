import { apiFetch } from "./client"
import type { Price } from "../types/api"

export function getPrices(symbol: string) {
  return apiFetch<Price[]>(`/prices/${symbol}`)
}
