import { useState } from "react"
import ChatWindow from "./components/ChatWindow"
import InputBar from "./components/InputBar"

export default function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const askQuestion = async (question) => {
    setMessages((prev) => [...prev, { role: "user", content: question }])
    setLoading(true)

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      })
      const data = await res.json()

      if (data.answer) {
        setMessages((prev) => [...prev, { role: "bot", content: data.answer, sources: data.sources }])
      } else {
        setMessages((prev) => [...prev, { role: "bot", content: "something went wrong, try again." }])
      }
    } catch {
      setMessages((prev) => [...prev, { role: "bot", content: "can't reach the server." }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <header style={{
        padding: "20px 32px",
        borderBottom: "1px solid var(--glass-border)",
        backdropFilter: "blur(20px)",
        background: "var(--glass)",
        display: "flex",
        alignItems: "center",
        gap: "12px"
      }}>
        <div style={{
          width: 36, height: 36, borderRadius: "10px",
          background: "var(--accent)", display: "flex",
          alignItems: "center", justifyContent: "center",
          fontSize: "18px"
        }}>🎓</div>
        <div>
          <div style={{ fontFamily: "Syne", fontWeight: 700, fontSize: "18px" }}>CampusGuideGPT</div>
          <div style={{ fontSize: "12px", color: "var(--text-muted)" }}>Hochschule Harz AI Assistant</div>
        </div>
        <div style={{
          marginLeft: "auto", display: "flex", alignItems: "center",
          gap: "6px", fontSize: "12px", color: "#4ade80"
        }}>
          <div style={{
            width: 7, height: 7, borderRadius: "50%",
            background: "#4ade80", animation: "pulse 2s infinite"
          }} />
          online
        </div>
      </header>

      <ChatWindow messages={messages} loading={loading} />
      <InputBar onSend={askQuestion} loading={loading} />

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>
    </div>
  )
}