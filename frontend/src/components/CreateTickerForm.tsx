import { useState } from "react"
import { createTicker } from "../api/tickers"
import { validateTickerInput } from "../utils/validation"

type CreateTickerFormProps = {
  onCreated: () => Promise<void>
}

function CreateTickerForm({ onCreated }: CreateTickerFormProps) {
  const [symbol, setSymbol] = useState("")
  const [name, setName] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // console.log("onCreated prop:", onCreated)

  const handleSubmit: React.SubmitEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault()

    const result = validateTickerInput(symbol)

    if (!result.valid) {
        setError(result.error)
        return
    }

    const normalizedSymbol = result.value

    try {
        // console.log("isSubmitting -> true")
        setIsSubmitting(true)

        // await new Promise((resolve) => setTimeout(resolve, 1000))

        setError(null)

        await createTicker({
            symbol: normalizedSymbol,
            name: name.trim() || undefined,
        })

        await onCreated()

        setSymbol("")
        setName("")
    } catch (err: unknown) {
        console.error("createTicker failed:", err)

        if (err instanceof Error) {
            setError(err.message)
        } else {
            setError("Unexpected error")
        }
    } finally {
        // console.log("isSubmitting -> false")
        setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h3>Add ticker</h3>

      <input
        placeholder="Symbol"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        disabled={isSubmitting}
      />

      <input
        placeholder="Name (optional)"
        value={name}
        onChange={(e) => setName(e.target.value)}
        disabled={isSubmitting}
      />

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Adding..." : "Add"}
      </button>

      {error && <p>{error}</p>}
    </form>
  )
}

export default CreateTickerForm