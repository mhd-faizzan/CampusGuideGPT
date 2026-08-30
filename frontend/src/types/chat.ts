export type Role = "user" | "assistant"

export interface Source {
  score: number
  question: string
}

export type MessageStatus = "pending" | "complete" | "error"

export interface ChatMessage {
  id: string
  role: Role
  content: string
  ts: number
  status?: MessageStatus
  sources?: Source[]
}

export interface Conversation {
  id: string
  title: string
  createdAt: number
  updatedAt: number
  messages?: ChatMessage[]
}
