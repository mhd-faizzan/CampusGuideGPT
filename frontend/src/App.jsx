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
      setMessages((prev) => [...prev, {
        role: "bot",
        content: data.answer || "something went wrong.",
        sources: data.sources || []
      }])
    } catch {
      setMessages((prev) => [...prev, { role: "bot", content: "can't reach the server." }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      height: "100vh",
      background: "#212121",
    }}>
      <ChatWindow messages={messages} loading={loading} />
      <InputBar onSend={askQuestion} loading={loading} />
    </div>
  )
}