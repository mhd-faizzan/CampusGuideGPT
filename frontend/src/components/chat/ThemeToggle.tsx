import { IconButton } from "../ui/IconButton"
import { MoonIcon, SunIcon } from "../ui/icons"
import { useTheme } from "../../hooks/useTheme"

export function ThemeToggle() {
  const { resolvedTheme, toggle } = useTheme()
  const nextIsDark = resolvedTheme === "light"

  return (
    <IconButton label={nextIsDark ? "Switch to dark theme" : "Switch to light theme"} onClick={toggle}>
      {nextIsDark ? <MoonIcon /> : <SunIcon />}
    </IconButton>
  )
}
