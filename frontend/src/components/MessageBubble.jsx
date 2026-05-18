import { useState } from "react"

export default function MessageBubble({ message }) {
  const [showSources, setShowSources] = useState(false)
  const isUser = message.role === "user"

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: isUser ? "flex-end" : "flex-start",
      gap: "8px",
    }}>
      <div style={{
        maxWidth: "75%",
        padding: "14px 18px",
        borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
        background: isUser ? "var(--accent)" : "var(--glass)",
        border: isUser ? "none" : "1px solid var(--glass-border)",
        backdropFilter: "blur(10px)",
        fontSize: "15px",
        lineHeight: "1.7",
        color: "var(--text)",
        whiteSpace: "pre-wrap",
      }}>
        {message.content}
      </div>

      {message.sources && message.sources.length > 0 && (
        <div style={{ maxWidth: "75%" }}>
          <button
            onClick={() => setShowSources(!showSources)}
            style={{
              background: "none",
              border: "1px solid var(--glass-border)",
              color: "var(--text-muted)",
              fontSize: "12px",
              padding: "4px 12px",
              borderRadius: "20px",
              cursor: "pointer",
            }}
          >
            {showSources ? "hide sources" : `view ${message.sources.length} sources`}
          </button>

          {showSources && (
            <div style={{ marginTop: "8px", display: "flex", flexDirection: "column", gap: "8px" }}>
              {message.sources.map((src, i) => (
                <div key={i} style={{
                  padding: "12px 16px",
                  background: "var(--glass)",
                  border: "1px solid var(--glass-border)",
                  borderLeft: "3px solid var(--accent)",
                  borderRadius: "10px",
                  fontSize: "13px",
                  backdropFilter: "blur(10px)",
                }}>
                  <div style={{ color: "var(--accent)", fontWeight: 500, marginBottom: "4px" }}>
                    {Math.round(src.score * 100)}% match
                  </div>
                  <div style={{ color: "var(--text-muted)" }}>{src.question}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}