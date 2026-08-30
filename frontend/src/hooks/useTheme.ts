import { useCallback, useEffect, useState } from "react"
import { useMediaQuery } from "./useMediaQuery"

export type ThemePref = "light" | "dark" | "system"
export type ResolvedTheme = "light" | "dark"

const STORAGE_KEY = "cg-theme"

function readPref(): ThemePref {
  try {
    const v = localStorage.getItem(STORAGE_KEY)
    if (v === "light" || v === "dark" || v === "system") return v
  } catch {
    // localStorage unavailable — fall through
  }
  return "system"
}

function apply(pref: ThemePref): void {
  const root = document.documentElement
  if (pref === "system") root.removeAttribute("data-theme")
  else root.setAttribute("data-theme", pref)
}

export interface ThemeControls {
  theme: ThemePref
  resolvedTheme: ResolvedTheme
  setTheme: (pref: ThemePref) => void
  toggle: () => void
}

export function useTheme(): ThemeControls {
  const [theme, setTheme] = useState<ThemePref>(readPref)
  const systemDark = useMediaQuery("(prefers-color-scheme: dark)")

  useEffect(() => {
    apply(theme)
    try {
      localStorage.setItem(STORAGE_KEY, theme)
    } catch {
      // ignore write failures (private mode, etc.)
    }
  }, [theme])

  const resolvedTheme: ResolvedTheme =
    theme === "system" ? (systemDark ? "dark" : "light") : theme

  const toggle = useCallback(() => {
    setTheme(resolvedTheme === "dark" ? "light" : "dark")
  }, [resolvedTheme])

  return { theme, resolvedTheme, setTheme, toggle }
}
