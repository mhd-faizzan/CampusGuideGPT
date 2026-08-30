import { useCallback, useState } from "react"
import type { User } from "firebase/auth"
import { ApiError, ask } from "../lib/api"
import { appendTurn, createConversation, getConversation } from "../lib/conversations"
import type { ChatMessage, Conversation } from "../types/chat"

function makeMessage(msg: Omit<ChatMessage, "id" | "ts">): ChatMessage {
  return { id: crypto.randomUUID(), ts: Date.now(), ...msg }
}

export interface ChatController {
  messages: ChatMessage[]
  activeId: string | null
  isSending: boolean
  sendMessage: (text: string) => Promise<void>
  openConversation: (conversation: Conversation) => void
  newChat: () => void
}

export function useChat(user: User): ChatController {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [activeId, setActiveId] = useState<string | null>(null)
  const [isSending, setIsSending] = useState(false)

  const patchLast = useCallback((patch: (m: ChatMessage) => ChatMessage) => {
    setMessages((prev) => {
      if (prev.length === 0) return prev
      const next = prev.slice()
      const last = next[next.length - 1]
      if (last) next[next.length - 1] = patch(last)
      return next
    })
  }, [])

  const newChat = useCallback(() => {
    if (isSending) return
    setActiveId(null)
    setMessages([])
  }, [isSending])

  const openConversation = useCallback(
    (conversation: Conversation) => {
      if (isSending || conversation.id === activeId) return
      setActiveId(conversation.id)
      setMessages(conversation.messages ?? [])
      // metadata list omits messages — hydrate the full doc
      void getConversation(user.uid, conversation.id).then((full) => {
        if (full) setMessages(full.messages ?? [])
      })
    },
    [isSending, activeId, user.uid],
  )

  const sendMessage = useCallback(
    async (text: string) => {
      const question = text.trim()
      if (!question || isSending) return

      const userMsg = makeMessage({ role: "user", content: question, status: "complete" })
      const pending = makeMessage({ role: "assistant", content: "", status: "pending" })
      setMessages((prev) => [...prev, userMsg, pending])
      setIsSending(true)

      try {
        const token = await user.getIdToken()
        const { answer, sources } = await ask(question, token)
        const answerMsg: ChatMessage = {
          ...pending,
          content: answer,
          sources,
          status: "complete",
        }
        patchLast(() => answerMsg)

        try {
          let convId = activeId
          if (!convId) {
            convId = await createConversation(user.uid, question)
            setActiveId(convId)
          }
          await appendTurn(user.uid, convId, userMsg, answerMsg)
        } catch (saveErr) {
          console.error("failed to save chat", saveErr)
        }
      } catch (err) {
        const message =
          err instanceof ApiError
            ? err.message
            : "can't reach the server. is the backend running?"
        patchLast((m) => ({ ...m, content: message, status: "error" }))
      } finally {
        setIsSending(false)
      }
    },
    [isSending, activeId, user, patchLast],
  )

  return { messages, activeId, isSending, sendMessage, openConversation, newChat }
}
