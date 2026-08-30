import { useEffect, useState } from "react"

/** Subscribe to a CSS media query. SSR-safe default of `false`. */
export function useMediaQuery(queryString: string): boolean {
  const [matches, setMatches] = useState(
    () => typeof window !== "undefined" && window.matchMedia(queryString).matches,
  )

  useEffect(() => {
    const mql = window.matchMedia(queryString)
    const onChange = () => setMatches(mql.matches)
    onChange()
    mql.addEventListener("change", onChange)
    return () => mql.removeEventListener("change", onChange)
  }, [queryString])

  return matches
}
