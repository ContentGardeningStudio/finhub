export type Ticker = {
  id: number
  symbol: string
  name?: string
}

export type Price = {
  date: string
  open?: number
  high?: number
  low?: number
  close?: number
  volume?: number
}

export type SyncResult = {
  symbol: string
  rows_downloaded: number
  rows_upserted: number
}