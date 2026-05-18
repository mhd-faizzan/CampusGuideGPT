import { useState } from "react"

export default function MessageBubble({ message }) {
  const [showSources, setShowSources] = useState(false)
  const isUser = message.role === "user"

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: isUser ? "flex-end" : "flex-start",
      gap: "6px",
    }}>
      {!isUser && (
        <div style={{ fontSize: "12px", color: "#8e8ea0", paddingLeft: "2px" }}>
          CampusGuideGPT
        </div>
      )}

      <div style={{
        maxWidth: "85%",
        padding: "12px 16px",
        borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
        background: isUser ? "#303030" : "#2a2a2a",
        fontSize: "15px",
        lineHeight: "1.7",
        color: "#ececec",
        whiteSpace: "pre-wrap",
        border: "1px solid #3a3a3a",
      }}>
        {message.content}
      </div>

      {message.sources && message.sources.length > 0 && (
        <div style={{ maxWidth: "85%" }}>
          <button
            onClick={() => setShowSources(!showSources)}
            style={{
              background: "none",
              border: "none",
              color: "#8e8ea0",
              fontSize: "12px",
              cursor: "pointer",
              padding: "2px 0",
              textDecoration: "underline",
            }}
          >
            {showSources ? "hide sources" : `${message.sources.length} sources`}
          </button>

          {showSources && (
            <div style={{ marginTop: "8px", display: "flex", flexDirection: "column", gap: "6px" }}>
              {message.sources.map((src, i) => (
                <div key={i} style={{
                  padding: "10px 14px",
                  background: "#2a2a2a",
                  border: "1px solid #3a3a3a",
                  borderLeft: "3px solid #8e8ea0",
                  borderRadius: "8px",
                  fontSize: "13px",
                  color: "#8e8ea0",
                }}>
                  <div style={{ marginBottom: "4px", color: "#ececec" }}>
                    {Math.round(src.score * 100)}% match
                  </div>
                  {src.question}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}