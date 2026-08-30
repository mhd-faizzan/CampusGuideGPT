import type { Source } from "../types/chat"

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

/** Non-2xx response from /ask, or a network failure (status 0). */
export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

export interface AskResult {
  answer: string
  sources: Source[]
}

function isAbort(err: unknown): boolean {
  return err instanceof Error && err.name === "AbortError"
}

function readError(data: unknown): string | null {
  if (data && typeof data === "object" && "error" in data) {
    const e = (data as { error: unknown }).error
    if (typeof e === "string" && e.trim()) return e
  }
  return null
}

function toSources(raw: unknown): Source[] {
  if (!Array.isArray(raw)) return []
  return raw.map((hit) => {
    const h = (hit ?? {}) as Record<string, unknown>
    return {
      score: typeof h.score === "number" ? h.score : 0,
      question: typeof h.question === "string" ? h.question : "",
    }
  })
}

/**
 * POST /ask and return the full answer. The backend is non-streaming — this
 * resolves once when the answer is ready. `signal` lets a caller abort (e.g. on
 * navigation); an abort rejects with an AbortError, not an ApiError.
 */
export async function ask(question: string, token: string, signal?: AbortSignal): Promise<AskResult> {
  let res: Response
  try {
    res = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ question }),
      signal,
    })
  } catch (err) {
    if (isAbort(err)) throw err
    throw new ApiError(0, "can't reach the server. is the backend running?")
  }

  let data: unknown = null
  try {
    data = await res.json()
  } catch {
    // non-JSON body — handled below
  }

  if (!res.ok) {
    const message =
      readError(data) ??
      (res.status === 429
        ? "too many requests. please slow down or come back tomorrow."
        : res.status >= 500
          ? "something went wrong on our end. try again."
          : "request failed")
    throw new ApiError(res.status, message)
  }

  const obj = (data ?? {}) as Record<string, unknown>
  return {
    answer: typeof obj.answer === "string" && obj.answer.trim() ? obj.answer : "no answer returned.",
    sources: toSources(obj.sources),
  }
}
