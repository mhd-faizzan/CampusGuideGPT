import { useCallback, useEffect, useRef } from "react"

const NEAR_BOTTOM_PX = 120

/**
 * Keeps a scroll container pinned to the bottom as content grows, but only while
 * the user hasn't scrolled up. Pass a signature string that changes whenever the
 * content height might have changed.
 */
export function useAutoScroll(signature: string) {
  const containerRef = useRef<HTMLDivElement>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const pinnedRef = useRef(true)

  const handleScroll = useCallback(() => {
    const el = containerRef.current
    if (!el) return
    pinnedRef.current = el.scrollHeight - el.scrollTop - el.clientHeight < NEAR_BOTTOM_PX
  }, [])

  useEffect(() => {
    if (pinnedRef.current) {
      bottomRef.current?.scrollIntoView({ block: "end", behavior: "smooth" })
    }
  }, [signature])

  return { containerRef, bottomRef, handleScroll }
}
