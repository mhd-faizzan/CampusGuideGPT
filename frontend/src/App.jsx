import { useState, useEffect } from "react"
import { onAuthStateChanged, signOut } from "firebase/auth"
import { auth } from "./firebase"
import ChatWindow from "./components/ChatWindow"
import InputBar from "./components/InputBar"
import Sidebar from "./components/Sidebar"
import Login from "./components/Login"
import VerifyEmail from "./components/VerifyEmail"
import {
  subscribeConversations,
  createConversation,
  getConversation,
  appendTurn,
  deleteConversation,
} from "./conversations"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

const GREETING = {
  role: "bot",
  content:
    "Hi! I'm CampusGuideGPT 🎓 Ask me anything about Hochschule Harz — admissions, campus life, accommodation, or programs.",
  sources: [],
}

export default function App() {
  const [user, setUser] = useState(null)
  const [authLoading, setAuthLoading] = useState(true)

  const [conversations, setConversations] = useState([])
  const [activeId, setActiveId] = useState(null) // null = unsaved new chat
  const [messages, setMessages] = useState([]) // real turns only (no greeting)
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (u) => {
      setUser(u)
      setAuthLoading(false)
      if (!u) {
        setConversations([])
        setActiveId(null)
        setMessages([])
      }
    })
    return unsub
  }, [])

  // live list of saved conversations for the signed-in user
  useEffect(() => {
    if (!user) return
    return subscribeConversations(user.uid, setConversations)
  }, [user])

  const startNewChat = () => {
    if (loading) return
    setActiveId(null)
    setMessages([])
  }

  const openConversation = async (id) => {
    if (loading || id === activeId) return
    const conv = await getConversation(user.uid, id)
    setActiveId(id)
    setMessages(conv?.messages || [])
  }

  const removeConversation = async (id) => {
    await deleteConversation(user.uid, id)
    if (id === activeId) startNewChat()
  }

  const askQuestion = async (question) => {
    const userMsg = { role: "user", content: question, ts: Date.now() }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)

    try {
      const token = await auth.currentUser.getIdToken()
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ question }),
      })

      const data = await res.json()

      if (res.status === 429) {
        setMessages((prev) => [
          ...prev,
          { role: "bot", content: data.error || "too many requests. please slow down or come back tomorrow." },
        ])
        return
      }

      if (res.status === 500) {
        setMessages((prev) => [...prev, { role: "bot", content: "something went wrong on our end. try again." }])
        return
      }

      const botMsg = {
        role: "bot",
        content: data.answer || "no answer returned.",
        sources: data.sources || [],
        ts: Date.now(),
      }
      setMessages((prev) => [...prev, botMsg])

      // persist the completed turn
      try {
        let convId = activeId
        if (!convId) {
          convId = await createConversation(user.uid, question)
          setActiveId(convId)
        }
        await appendTurn(user.uid, convId, userMsg, botMsg)
      } catch (err) {
        console.error("failed to save chat", err)
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "can't reach the server. is the backend running?" },
      ])
    } finally {
      setLoading(false)
    }
  }

  if (authLoading) return null
  if (!user) return <Login />
  if (!user.emailVerified) return <VerifyEmail />

  const view = messages.length ? messages : [GREETING]

  return (
    <div style={{ display: "flex", height: "100vh", background: "#212121" }}>
      <Sidebar
        open={sidebarOpen}
        conversations={conversations}
        activeId={activeId}
        onSelect={openConversation}
        onNew={startNewChat}
        onDelete={removeConversation}
        disabled={loading}
      />

      <div style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: 8,
          }}
        >
          <button
            onClick={() => setSidebarOpen((v) => !v)}
            title={sidebarOpen ? "Hide sidebar" : "Show sidebar"}
            style={{
              background: "none",
              border: "none",
              color: "#8e8ea0",
              cursor: "pointer",
              fontSize: 18,
              padding: "2px 8px",
            }}
          >
            ☰
          </button>
          <button
            onClick={() => signOut(auth)}
            style={{ background: "none", border: "none", color: "#8e8ea0", cursor: "pointer", fontSize: 13 }}
          >
            Sign out
          </button>
        </div>

        <ChatWindow messages={view} loading={loading} />
        <InputBar onSend={askQuestion} loading={loading} />
      </div>
    </div>
  )
}
