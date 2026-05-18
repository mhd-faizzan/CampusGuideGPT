import { useEffect, useRef } from "react"
import MessageBubble from "./MessageBubble"

export default function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  return (
    <div style={{
      flex: 1,
      overflowY: "auto",
      padding: "32px 24px",
      display: "flex",
      flexDirection: "column",
      gap: "16px",
      maxWidth: "800px",
      width: "100%",
      margin: "0 auto",
    }}>
      {messages.length === 0 && (
        <div style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: "16px",
          opacity: 0.5,
          paddingTop: "80px",
        }}>
          <div style={{ fontSize: "48px" }}>🎓</div>
          <div style={{ fontFamily: "Syne", fontSize: "20px", fontWeight: 600 }}>
            Ask me anything
          </div>
          <div style={{ fontSize: "14px", color: "var(--text-muted)", textAlign: "center" }}>
            admissions, campus life, programs, accommodation
          </div>
        </div>
      )}

      {messages.map((msg, i) => (
        <MessageBubble key={i} message={msg} />
      ))}

      {loading && (
        <div style={{
          display: "flex",
          gap: "6px",
          padding: "16px 20px",
          background: "var(--glass)",
          border: "1px solid var(--glass-border)",
          borderRadius: "16px",
          width: "fit-content",
          backdropFilter: "blur(10px)",
        }}>
          {[0, 1, 2].map((i) => (
            <div key={i} style={{
              width: 8, height: 8,
              borderRadius: "50%",
              background: "var(--accent)",
              animation: `bounce 1s infinite ${i * 0.15}s`,
            }} />
          ))}
          <style>{`
            @keyframes bounce {
              0%, 100% { transform: translateY(0); }
              50% { transform: translateY(-6px); }
            }
          `}</style>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}