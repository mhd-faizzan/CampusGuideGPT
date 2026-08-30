import {
  collection,
  doc,
  addDoc,
  getDoc,
  updateDoc,
  deleteDoc,
  onSnapshot,
  query,
  orderBy,
  arrayUnion,
} from "firebase/firestore"
import { db } from "./firebase"
import type { ChatMessage, Conversation, Role, Source } from "../types/chat"

// users/{uid}/conversations/{id}
//   title, createdAt, updatedAt, messages: [{ id, role, content, ts, sources }]

const convCollection = (uid: string) => collection(db, "users", uid, "conversations")
const convDoc = (uid: string, id: string) => doc(db, "users", uid, "conversations", id)

function titleFrom(text: string): string {
  const clean = text.trim().replace(/\s+/g, " ")
  return clean.length > 48 ? `${clean.slice(0, 48)}…` : clean
}

/** Strip transient fields before writing; keep only what we render on reload. */
function toStored(msg: ChatMessage) {
  return {
    id: msg.id,
    role: msg.role,
    content: msg.content,
    ts: msg.ts,
    sources: (msg.sources ?? []).map((s) => ({ score: s.score, question: s.question })),
  }
}

function num(v: unknown, fallback: number): number {
  return typeof v === "number" && Number.isFinite(v) ? v : fallback
}

function normalizeRole(v: unknown): Role {
  return v === "user" ? "user" : "assistant" // legacy docs use "bot"
}

function normalizeSources(v: unknown): Source[] {
  if (!Array.isArray(v)) return []
  return v.map((s) => {
    const o = (s ?? {}) as Record<string, unknown>
    return {
      score: num(o.score, 0),
      question: typeof o.question === "string" ? o.question : "",
    }
  })
}

function normalizeMessage(v: unknown, index: number): ChatMessage {
  const o = (v ?? {}) as Record<string, unknown>
  return {
    id: typeof o.id === "string" ? o.id : `legacy-${index}`,
    role: normalizeRole(o.role),
    content: typeof o.content === "string" ? o.content : "",
    ts: num(o.ts, Date.now() + index),
    status: "complete",
    sources: normalizeSources(o.sources),
  }
}

function normalizeConversation(id: string, data: Record<string, unknown>): Conversation {
  const rawMessages = Array.isArray(data.messages) ? data.messages : []
  return {
    id,
    title: typeof data.title === "string" && data.title.trim() ? data.title : "Untitled",
    createdAt: num(data.createdAt, 0),
    updatedAt: num(data.updatedAt, 0),
    messages: rawMessages.map(normalizeMessage),
  }
}

/** Live list of the user's conversations, newest first (metadata only). */
export function subscribeConversations(
  uid: string,
  onChange: (conversations: Conversation[]) => void,
): () => void {
  const q = query(convCollection(uid), orderBy("updatedAt", "desc"))
  return onSnapshot(q, (snap) => {
    onChange(
      snap.docs.map((d) => {
        // list view is metadata only — drop the messages array
        const { id, title, createdAt, updatedAt } = normalizeConversation(d.id, d.data())
        return { id, title, createdAt, updatedAt }
      }),
    )
  })
}

export async function createConversation(uid: string, firstQuestion: string): Promise<string> {
  const now = Date.now()
  const ref = await addDoc(convCollection(uid), {
    title: titleFrom(firstQuestion),
    createdAt: now,
    updatedAt: now,
    messages: [],
  })
  return ref.id
}

export async function getConversation(uid: string, id: string): Promise<Conversation | null> {
  const snap = await getDoc(convDoc(uid, id))
  return snap.exists() ? normalizeConversation(snap.id, snap.data()) : null
}

/** Append one completed turn (user question + assistant answer). */
export async function appendTurn(
  uid: string,
  id: string,
  userMsg: ChatMessage,
  assistantMsg: ChatMessage,
): Promise<void> {
  await updateDoc(convDoc(uid, id), {
    messages: arrayUnion(toStored(userMsg), toStored(assistantMsg)),
    updatedAt: Date.now(),
  })
}

export async function renameConversation(uid: string, id: string, title: string): Promise<void> {
  await updateDoc(convDoc(uid, id), { title: title.trim() || "Untitled" })
}

export async function deleteConversation(uid: string, id: string): Promise<void> {
  await deleteDoc(convDoc(uid, id))
}
