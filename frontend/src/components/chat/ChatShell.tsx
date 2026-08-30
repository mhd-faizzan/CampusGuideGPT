import { useEffect, useState } from "react"
import { signOut, type User } from "firebase/auth"
import { auth } from "../../lib/firebase"
import { deleteConversation } from "../../lib/conversations"
import { useChat } from "../../hooks/useChat"
import { useConversations } from "../../hooks/useConversations"
import { useMediaQuery } from "../../hooks/useMediaQuery"
import { useFocusTrap } from "../../hooks/useFocusTrap"
import type { Conversation } from "../../types/chat"
import { Header } from "./Header"
import { Sidebar } from "./Sidebar"
import { MessageList } from "./MessageList"
import { Composer } from "./Composer"
import { EmptyState } from "./EmptyState"

const DESKTOP_QUERY = "(min-width: 768px)"

interface ChatShellProps {
  user: User
}

export function ChatShell({ user }: ChatShellProps) {
  const conversations = useConversations(user.uid)
  const { messages, activeId, isSending, sendMessage, openConversation, newChat } = useChat(user)

  const isDesktop = useMediaQuery(DESKTOP_QUERY)
  const [sidebarOpen, setSidebarOpen] = useState(false) // closed by default

  // collapse the sidebar when the viewport shrinks to mobile; never force it open
  useEffect(() => {
    const mql = window.matchMedia(DESKTOP_QUERY)
    const onChange = () => {
      if (!mql.matches) setSidebarOpen(false)
    }
    mql.addEventListener("change", onChange)
    return () => mql.removeEventListener("change", onChange)
  }, [])

  const drawerOpen = !isDesktop && sidebarOpen
  const drawerRef = useFocusTrap<HTMLDivElement>(drawerOpen, () => setSidebarOpen(false))

  useEffect(() => {
    if (!drawerOpen) return
    const prev = document.body.style.overflow
    document.body.style.overflow = "hidden"
    return () => {
      document.body.style.overflow = prev
    }
  }, [drawerOpen])

  const closeOnMobile = () => {
    if (!isDesktop) setSidebarOpen(false)
  }

  const handleSelect = (conversation: Conversation) => {
    openConversation(conversation)
    closeOnMobile()
  }

  const handleNew = () => {
    newChat()
    closeOnMobile()
  }

  const handleDelete = (id: string) => {
    void deleteConversation(user.uid, id).catch((err) => console.error("failed to delete chat", err))
    if (id === activeId) newChat()
  }

  const sidebar = (
    <Sidebar
      conversations={conversations}
      activeId={activeId}
      disabled={isSending}
      onSelect={handleSelect}
      onNew={handleNew}
      onDelete={handleDelete}
    />
  )

  return (
    <div className="flex h-dvh overflow-hidden bg-canvas text-fg">
      {/* desktop: collapsible rail */}
      <aside
        className="hidden shrink-0 overflow-hidden transition-[width] duration-200 ease-out md:block"
        style={{ width: isDesktop && sidebarOpen ? 260 : 0 }}
      >
        {sidebar}
      </aside>

      {/* mobile: drawer */}
      {drawerOpen && (
        <div className="fixed inset-0 z-40 md:hidden">
          <div
            className="absolute inset-0 bg-black/50"
            onClick={() => setSidebarOpen(false)}
            aria-hidden
          />
          <div ref={drawerRef} role="dialog" aria-label="Chat history" className="absolute inset-y-0 left-0 shadow-xl">
            {sidebar}
          </div>
        </div>
      )}

      <div className="flex min-w-0 flex-1 flex-col">
        <Header
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen((v) => !v)}
          onNewChat={handleNew}
          onSignOut={() => void signOut(auth)}
        />

        {messages.length === 0 ? (
          <div className="flex flex-1 flex-col items-center justify-center gap-7 overflow-y-auto px-4">
            <EmptyState name={user.displayName?.trim().split(/\s+/)[0]} />
            <div className="w-full">
              <Composer onSend={sendMessage} isSending={isSending} />
            </div>
          </div>
        ) : (
          <>
            <MessageList messages={messages} />
            <Composer onSend={sendMessage} isSending={isSending} />
          </>
        )}
      </div>
    </div>
  )
}
