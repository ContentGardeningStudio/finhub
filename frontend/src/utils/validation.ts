type ValidationResult =
  | { valid: true; value: string }
  | { valid: false; error: string }

export function validateTickerInput(symbol: string): ValidationResult {
  const normalized = symbol.trim().toUpperCase()

  if (!normalized) {
    return { valid: false, error: "Symbol is required" }
  }

  if (normalized.length > 10) {
    return { valid: false, error: "Symbol is too long" }
  }

  return { valid: true, value: normalized }
}