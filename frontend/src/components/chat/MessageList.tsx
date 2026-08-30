import { useAutoScroll } from "../../hooks/useAutoScroll"
import type { ChatMessage } from "../../types/chat"
import { Message } from "./Message"

interface MessageListProps {
  messages: ChatMessage[]
}

export function MessageList({ messages }: MessageListProps) {
  const last = messages[messages.length - 1]
  const signature = `${messages.length}:${last?.content.length ?? 0}:${last?.status ?? ""}`
  const { containerRef, bottomRef, handleScroll } = useAutoScroll(signature)

  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      className="flex-1 overflow-y-auto"
      role="log"
      aria-live="polite"
      aria-label="Conversation"
    >
      <div className="mx-auto flex w-full max-w-[768px] flex-col gap-9 px-4 py-12 sm:px-6">
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        <div ref={bottomRef} className="h-2" />
      </div>
    </div>
  )
}
