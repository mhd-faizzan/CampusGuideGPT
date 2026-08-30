import { useEffect, useState } from "react"
import { subscribeConversations } from "../lib/conversations"
import type { Conversation } from "../types/chat"

/** Live list of the signed-in user's conversations, newest first. */
export function useConversations(uid: string | undefined): Conversation[] {
  const [conversations, setConversations] = useState<Conversation[]>([])

  useEffect(() => {
    if (!uid) return
    const unsubscribe = subscribeConversations(uid, setConversations)
    return () => {
      unsubscribe()
      setConversations([])
    }
  }, [uid])

  return conversations
}
