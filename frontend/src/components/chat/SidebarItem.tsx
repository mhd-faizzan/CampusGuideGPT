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
        "group relative flex items-center rounded-lg pr-1 transition-colors duration-100",
        isActive ? "bg-fg/[0.07]" : "hover:bg-fg/[0.04]",
      )}
    >
      <button
        type="button"
        onClick={onSelect}
        disabled={disabled}
        aria-current={isActive ? "page" : undefined}
        className={cn(
          "min-w-0 flex-1 truncate rounded-lg px-2.5 py-2 text-left text-[13px] outline-none transition-colors focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50",
          isActive ? "text-fg" : "text-muted group-hover:text-fg",
        )}
      >
        {title}
      </button>
      <IconButton
        label="Delete chat"
        disabled={disabled}
        onClick={onDelete}
        className="size-7 opacity-0 transition-opacity group-hover:opacity-100 focus-visible:opacity-100"
      >
        <TrashIcon />
      </IconButton>
    </div>
  )
}
