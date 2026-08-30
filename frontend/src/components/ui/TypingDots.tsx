export function TypingDots() {
  return (
    <div className="flex items-center gap-1 py-1" role="status" aria-label="Assistant is typing">
      <span className="typing-dot" style={{ animationDelay: "0s" }} />
      <span className="typing-dot" style={{ animationDelay: "0.15s" }} />
      <span className="typing-dot" style={{ animationDelay: "0.3s" }} />
    </div>
  )
}
