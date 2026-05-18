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