import { useState, useEffect } from "react"
import { onAuthStateChanged, signOut } from "firebase/auth"
import { auth } from "./firebase"
import ChatWindow from "./components/ChatWindow"
import InputBar from "./components/InputBar"
import Login from "./components/Login"
import VerifyEmail from "./components/VerifyEmail"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export default function App() {
  const [user, setUser] = useState(null)
  const [authLoading, setAuthLoading] = useState(true)

  const [messages, setMessages] = useState([
    {
      role: "bot",
      content: "Hi! I'm CampusGuideGPT 🎓 Ask me anything about Hochschule Harz — admissions, campus life, accommodation, or programs.",
      sources: [],
    }
  ])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (u) => {
      setUser(u)
      setAuthLoading(false)
    })
    return unsub
  }, [])

    const askQuestion = async (question) => {
    setMessages((prev) => [...prev, { role: "user", content: question }])
    setLoading(true)

    try {
      const token = await auth.currentUser.getIdToken()
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ question }),
      })

      const data = await res.json()

      if (res.status === 429) {
        setMessages((prev) => [...prev, {
          role: "bot",
          content: data.error || "too many requests. please slow down or come back tomorrow.",
        }])
        return
      }

      if (res.status === 500) {
        setMessages((prev) => [...prev, {
          role: "bot",
          content: "something went wrong on our end. try again.",
        }])
        return
      }

      setMessages((prev) => [...prev, {
        role: "bot",
        content: data.answer || "no answer returned.",
        sources: data.sources || [],
      }])

    } catch {
      setMessages((prev) => [...prev, {
        role: "bot",
        content: "can't reach the server. is the backend running?",
      }])
    } finally {
      setLoading(false)
    }
  }

  if (authLoading) return null
  if (!user) return <Login />
  if (!user.emailVerified) return <VerifyEmail />

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      height: "100vh",
      background: "#212121",
    }}>
      <div style={{ display: "flex", justifyContent: "flex-end", padding: 8 }}>
        <button onClick={() => signOut(auth)} style={{
          background: "none", border: "none", color: "#8e8ea0", cursor: "pointer", fontSize: 13,
        }}>
          Sign out
        </button>
      </div>
      <ChatWindow messages={messages} loading={loading} />
      <InputBar onSend={askQuestion} loading={loading} />
    </div>
  )
}