import { useState } from "react"

export default function InputBar({ onSend, loading }) {
  const [input, setInput] = useState("")

  const handleSend = () => {
    if (!input.trim() || loading) return
    onSend(input.trim())
    setInput("")
  }

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div style={{
      padding: "16px 24px 24px",
      borderTop: "1px solid var(--glass-border)",
      backdropFilter: "blur(20px)",
      background: "var(--glass)",
    }}>
      <div style={{
        maxWidth: "800px",
        margin: "0 auto",
        display: "flex",
        gap: "12px",
        alignItems: "flex-end",
      }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="ask anything about Hochschule Harz..."
          rows={1}
          style={{
            flex: 1,
            background: "var(--glass)",
            border: "1px solid var(--glass-border)",
            borderRadius: "14px",
            padding: "14px 18px",
            color: "var(--text)",
            fontSize: "15px",
            resize: "none",
            outline: "none",
            fontFamily: "DM Sans, sans-serif",
            lineHeight: "1.5",
            transition: "border 0.2s",
          }}
          onFocus={(e) => e.target.style.border = "1px solid var(--accent)"}
          onBlur={(e) => e.target.style.border = "1px solid var(--glass-border)"}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          style={{
            width: "48px",
            height: "48px",
            borderRadius: "14px",
            background: loading || !input.trim() ? "var(--glass)" : "var(--accent)",
            border: "1px solid var(--glass-border)",
            color: "var(--text)",
            fontSize: "20px",
            cursor: loading || !input.trim() ? "not-allowed" : "pointer",
            transition: "all 0.2s",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {loading ? "⏳" : "↑"}
        </button>
      </div>
      <div style={{
        textAlign: "center",
        fontSize: "11px",
        color: "var(--text-muted)",
        marginTop: "10px",
        maxWidth: "800px",
        margin: "10px auto 0",
      }}>
        press enter to send · shift+enter for new line
      </div>
    </div>
  )
}