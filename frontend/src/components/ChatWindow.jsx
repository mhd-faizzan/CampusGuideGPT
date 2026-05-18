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
      display: "flex",
      flexDirection: "column",
    }}>
      {messages.length === 0 ? (
        <div style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: "12px",
        }}>
          <div style={{ fontSize: "36px" }}>🎓</div>
          <div style={{
            fontSize: "22px",
            fontWeight: 600,
            color: "#ececec",
          }}>
            CampusGuideGPT
          </div>
          <div style={{ fontSize: "14px", color: "#8e8ea0" }}>
            your AI guide for Hochschule Harz
          </div>
        </div>
      ) : (
        <div style={{
          maxWidth: "680px",
          width: "100%",
          margin: "0 auto",
          padding: "40px 24px",
          display: "flex",
          flexDirection: "column",
          gap: "24px",
        }}>
          {messages.map((msg, i) => (
            <MessageBubble key={i} message={msg} />
          ))}

          {loading && (
            <div style={{ display: "flex", gap: "4px", paddingLeft: "4px" }}>
              {[0, 1, 2].map((i) => (
                <div key={i} style={{
                  width: 7, height: 7,
                  borderRadius: "50%",
                  background: "#8e8ea0",
                  animation: `bounce 1s infinite ${i * 0.15}s`,
                }} />
              ))}
              <style>{`
                @keyframes bounce {
                  0%, 100% { transform: translateY(0); opacity: 0.4; }
                  50% { transform: translateY(-5px); opacity: 1; }
                }
              `}</style>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      )}
    </div>
  )
}