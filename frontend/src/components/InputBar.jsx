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
      padding: "12px 24px 24px",
      background: "#212121",
    }}>
      <div style={{
        maxWidth: "680px",
        margin: "0 auto",
        display: "flex",
        alignItems: "flex-end",
        gap: "8px",
        background: "#2f2f2f",
        border: "1px solid #3f3f3f",
        borderRadius: "16px",
        padding: "12px 16px",
      }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Message CampusGuideGPT..."
          rows={1}
          style={{
            flex: 1,
            background: "none",
            border: "none",
            outline: "none",
            color: "#ececec",
            fontSize: "15px",
            resize: "none",
            fontFamily: "inherit",
            lineHeight: "1.5",
            maxHeight: "120px",
            overflowY: "auto",
          }}
          onInput={(e) => {
            e.target.style.height = "auto"
            e.target.style.height = e.target.scrollHeight + "px"
          }}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          style={{
            width: "32px",
            height: "32px",
            borderRadius: "8px",
            background: loading || !input.trim() ? "#3f3f3f" : "#ececec",
            border: "none",
            color: loading || !input.trim() ? "#8e8ea0" : "#212121",
            fontSize: "16px",
            cursor: loading || !input.trim() ? "not-allowed" : "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
            transition: "all 0.15s",
          }}
        >
          ↑
        </button>
      </div>
      <div style={{
        textAlign: "center",
        fontSize: "11px",
        color: "#8e8ea0",
        marginTop: "8px",
      }}>
        press enter to send · shift+enter for new line
      </div>
    </div>
  )
}