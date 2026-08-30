import { Button } from "../ui/Button"
import { IconButton } from "../ui/IconButton"
import { MenuIcon } from "../ui/icons"
import { ThemeToggle } from "./ThemeToggle"

interface HeaderProps {
  sidebarOpen: boolean
  onToggleSidebar: () => void
  onSignOut: () => void
}

export function Header({ sidebarOpen, onToggleSidebar, onSignOut }: HeaderProps) {
  return (
    <header className="flex h-12 shrink-0 items-center justify-between px-2 sm:px-3">
      <div className="flex items-center gap-1">
        <IconButton
          label={sidebarOpen ? "Hide sidebar" : "Show sidebar"}
          aria-expanded={sidebarOpen}
          onClick={onToggleSidebar}
        >
          <MenuIcon />
        </IconButton>
        <span className="text-sm text-muted">CampusGuideGPT</span>
      </div>
      <div className="flex items-center gap-1">
        <ThemeToggle />
        <Button variant="ghost" size="sm" onClick={onSignOut}>
          Sign out
        </Button>
      </div>
    </header>
  )
}
