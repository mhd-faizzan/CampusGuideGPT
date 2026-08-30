import { Button } from "../ui/Button"
import { PlusIcon } from "../ui/icons"
import { SidebarItem } from "./SidebarItem"
import type { Conversation } from "../../types/chat"

interface SidebarProps {
  conversations: Conversation[]
  activeId: string | null
  disabled: boolean
  onSelect: (conversation: Conversation) => void
  onNew: () => void
  onDelete: (id: string) => void
}

export function Sidebar({
  conversations,
  activeId,
  disabled,
  onSelect,
  onNew,
  onDelete,
}: SidebarProps) {
  return (
    <div className="flex h-full w-[260px] flex-col bg-sidebar">
      <div className="p-2.5">
        <Button
          variant="ghost"
          size="sm"
          className="w-full justify-start gap-2 text-muted hover:text-fg"
          onClick={onNew}
          disabled={disabled}
        >
          <PlusIcon width={16} height={16} />
          New chat
        </Button>
      </div>

      <nav aria-label="Chat history" className="flex-1 overflow-y-auto px-2 pb-3">
        {conversations.length === 0 ? (
          <p className="px-2.5 py-2 text-[13px] text-faint">No saved chats yet</p>
        ) : (
          <ul className="flex flex-col gap-px">
            {conversations.map((conversation) => (
              <li key={conversation.id}>
                <SidebarItem
                  title={conversation.title}
                  isActive={conversation.id === activeId}
                  disabled={disabled}
                  onSelect={() => onSelect(conversation)}
                  onDelete={() => {
                    if (window.confirm("Delete this chat?")) onDelete(conversation.id)
                  }}
                />
              </li>
            ))}
          </ul>
        )}
      </nav>
    </div>
  )
}
