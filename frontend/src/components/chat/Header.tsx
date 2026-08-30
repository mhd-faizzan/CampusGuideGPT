import { Button } from "../ui/Button"
import { IconButton } from "../ui/IconButton"
import { PlusIcon, SidebarIcon } from "../ui/icons"
import { ThemeToggle } from "./ThemeToggle"

interface HeaderProps {
  sidebarOpen: boolean
  onToggleSidebar: () => void
  onNewChat: () => void
  onSignOut: () => void
}

export function Header({ sidebarOpen, onToggleSidebar, onNewChat, onSignOut }: HeaderProps) {
  return (
    <header className="flex h-14 shrink-0 items-center justify-between px-2 sm:px-3">
      <div className="flex items-center gap-0.5">
        <IconButton
          label={sidebarOpen ? "Hide sidebar" : "Show sidebar"}
          aria-expanded={sidebarOpen}
          onClick={onToggleSidebar}
        >
          <SidebarIcon />
        </IconButton>
        <IconButton label="New chat" onClick={onNewChat}>
          <PlusIcon />
        </IconButton>
      </div>
      <div className="flex items-center gap-0.5">
        <ThemeToggle />
        <Button variant="ghost" size="sm" className="text-muted hover:text-fg" onClick={onSignOut}>
          Sign out
        </Button>
      </div>
    </header>
  )
}
