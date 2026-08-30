import { useState } from "react"

export default function Sidebar({
  open,
  conversations,
  activeId,
  onSelect,
  onNew,
  onDelete,
  disabled,
}) {
  const [hoverId, setHoverId] = useState(null)

  return (
    <div
      style={{
        width: open ? 260 : 0,
        flexShrink: 0,
        background: "#171717",
        overflow: "hidden",
        transition: "width 0.2s ease",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div style={{ width: 260, display: "flex", flexDirection: "column", height: "100%" }}>
        <div style={{ padding: 12 }}>
          <button
            onClick={onNew}
            disabled={disabled}
            style={{
              width: "100%",
              padding: "10px 12px",
              borderRadius: 10,
              border: "1px solid #3a3a3a",
              background: "transparent",
              color: "#ececec",
              fontSize: 14,
              cursor: disabled ? "not-allowed" : "pointer",
              textAlign: "left",
              opacity: disabled ? 0.5 : 1,
            }}
          >
            + New chat
          </button>
        </div>

        <div style={{ flex: 1, overflowY: "auto", padding: "0 8px 12px" }}>
          {conversations.length === 0 ? (
            <div style={{ padding: "8px 12px", fontSize: 12, color: "#8e8ea0" }}>
              no saved chats yet
            </div>
          ) : (
            conversations.map((c) => {
              const isActive = c.id === activeId
              return (
                <div
                  key={c.id}
                  onMouseEnter={() => setHoverId(c.id)}
                  onMouseLeave={() => setHoverId(null)}
                  onClick={() => !disabled && onSelect(c.id)}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                    padding: "9px 10px",
                    borderRadius: 8,
                    marginBottom: 2,
                    cursor: disabled ? "not-allowed" : "pointer",
                    background: isActive ? "#2f2f2f" : hoverId === c.id ? "#232323" : "transparent",
                  }}
                >
                  <span
                    style={{
                      flex: 1,
                      fontSize: 13,
                      color: isActive ? "#ececec" : "#c5c5c5",
                      whiteSpace: "nowrap",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                    }}
                  >
                    {c.title || "Untitled"}
                  </span>
                  {(hoverId === c.id || isActive) && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        if (window.confirm("Delete this chat?")) onDelete(c.id)
                      }}
                      title="Delete chat"
                      style={{
                        background: "none",
                        border: "none",
                        color: "#8e8ea0",
                        cursor: "pointer",
                        fontSize: 14,
                        lineHeight: 1,
                        padding: 2,
                      }}
                    >
                      ×
                    </button>
                  )}
                </div>
              )
            })
          )}
        </div>
      </div>
    </div>
  )
}
