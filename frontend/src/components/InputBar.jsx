import { useState } from "react"

const MAX_LENGTH = 500

export default function InputBar({ onSend, loading }) {
  const [input, setInput] = useState("")

  const handleSend = () => {
    if (!input.trim() || loading || input.length > MAX_LENGTH) return
    onSend(input.trim())
    setInput("")
  }

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const remaining = MAX_LENGTH - input.length
  const isOverLimit = input.length > MAX_LENGTH

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
        border: `1px solid ${isOverLimit ? "#ef4444" : "#3f3f3f"}`,
        borderRadius: "16px",
        padding: "12px 16px",
        transition: "border 0.2s",
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
          disabled={loading || !input.trim() || isOverLimit}
          style={{
            width: "32px",
            height: "32px",
            borderRadius: "8px",
            background: loading || !input.trim() || isOverLimit ? "#3f3f3f" : "#ececec",
            border: "none",
            color: loading || !input.trim() || isOverLimit ? "#8e8ea0" : "#212121",
            fontSize: "16px",
            cursor: loading || !input.trim() || isOverLimit ? "not-allowed" : "pointer",
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
        maxWidth: "680px",
        margin: "6px auto 0",
        display: "flex",
        justifyContent: "space-between",
        fontSize: "11px",
        color: isOverLimit ? "#ef4444" : "#8e8ea0",
      }}>
        <span>press enter to send · shift+enter for new line</span>
        <span>{remaining}</span>
      </div>
    </div>
  )
}