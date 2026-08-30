import { cn } from "../../lib/cn"
import { IconButton } from "../ui/IconButton"
import { TrashIcon } from "../ui/icons"

interface SidebarItemProps {
  title: string
  isActive: boolean
  disabled: boolean
  onSelect: () => void
  onDelete: () => void
}

export function SidebarItem({ title, isActive, disabled, onSelect, onDelete }: SidebarItemProps) {
  return (
    <div
      className={cn(
        "group relative flex items-center rounded-lg pr-1 transition-colors",
        isActive ? "bg-surface" : "hover:bg-surface/60",
      )}
    >
      {isActive && (
        <span className="absolute inset-y-1.5 left-0 w-0.5 rounded-full bg-accent" aria-hidden />
      )}
      <button
        type="button"
        onClick={onSelect}
        disabled={disabled}
        aria-current={isActive ? "page" : undefined}
        className="min-w-0 flex-1 truncate px-3 py-2.5 text-left text-[13px] text-fg outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50"
      >
        {title}
      </button>
      <IconButton
        label="Delete chat"
        disabled={disabled}
        onClick={onDelete}
        className="size-8 opacity-0 group-hover:opacity-100 focus-visible:opacity-100"
      >
        <TrashIcon />
      </IconButton>
    </div>
  )
}
