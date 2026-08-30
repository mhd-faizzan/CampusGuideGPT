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

// users/{uid}/conversations/{conversationId}
//   title, createdAt, updatedAt, messages: [{ role, content, sources, ts }]

const convCollection = (uid) => collection(db, "users", uid, "conversations")
const convDoc = (uid, id) => doc(db, "users", uid, "conversations", id)

const titleFrom = (text) => {
  const clean = text.trim().replace(/\s+/g, " ")
  return clean.length > 48 ? clean.slice(0, 48) + "…" : clean
}

// keep stored messages lean — only what we render on reload
export const cleanMessage = (msg) => ({
  role: msg.role,
  content: msg.content,
  sources: (msg.sources || []).map((s) => ({
    score: s.score ?? 0,
    question: s.question ?? "",
  })),
  ts: msg.ts ?? Date.now(),
})

// live list of the user's conversations, newest first
export function subscribeConversations(uid, onChange) {
  const q = query(convCollection(uid), orderBy("updatedAt", "desc"))
  return onSnapshot(q, (snap) => {
    onChange(snap.docs.map((d) => ({ id: d.id, ...d.data() })))
  })
}

export async function createConversation(uid, firstQuestion) {
  const now = Date.now()
  const ref = await addDoc(convCollection(uid), {
    title: titleFrom(firstQuestion),
    createdAt: now,
    updatedAt: now,
    messages: [],
  })
  return ref.id
}

export async function getConversation(uid, id) {
  const snap = await getDoc(convDoc(uid, id))
  return snap.exists() ? { id: snap.id, ...snap.data() } : null
}

// append one completed turn (user question + bot answer)
export async function appendTurn(uid, id, userMsg, botMsg) {
  await updateDoc(convDoc(uid, id), {
    messages: arrayUnion(cleanMessage(userMsg), cleanMessage(botMsg)),
    updatedAt: Date.now(),
  })
}

export async function renameConversation(uid, id, title) {
  await updateDoc(convDoc(uid, id), { title: title.trim() || "Untitled" })
}

export async function deleteConversation(uid, id) {
  await deleteDoc(convDoc(uid, id))
}
