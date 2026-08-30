import { useId, useLayoutEffect, useRef, useState, type KeyboardEvent } from "react"
import { cn } from "../../lib/cn"
import { Spinner } from "../ui/Spinner"
import { ArrowUpIcon } from "../ui/icons"

const MAX_LENGTH = 500

interface ComposerProps {
  onSend: (text: string) => void
  isSending: boolean
}

export function Composer({ onSend, isSending }: ComposerProps) {
  const [value, setValue] = useState("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const labelId = useId()

  const trimmed = value.trim()
  const overLimit = value.length > MAX_LENGTH
  const canSend = trimmed.length > 0 && !isSending && !overLimit

  useLayoutEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = "auto"
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`
  }, [value])

  const submit = () => {
    if (!canSend) return
    onSend(trimmed)
    setValue("")
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  return (
    <div className="mx-auto w-full max-w-[768px] px-4 pb-6 pt-3 sm:px-6">
      <div
        className="flex items-end gap-1.5 rounded-[1.75rem] p-2 pl-4"
        style={{
          background: "var(--composer-bg)",
          backdropFilter: "blur(12px)",
          WebkitBackdropFilter: "blur(12px)",
          boxShadow: "0 0 0 1px rgba(255, 255, 255, 0.06), 0 8px 30px rgba(0, 0, 0, 0.3)",
        }}
      >
        <span id={labelId} className="sr-only">
          Message CampusGuideGPT
        </span>
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          aria-labelledby={labelId}
          placeholder="Message CampusGuideGPT…"
          className="max-h-[200px] flex-1 resize-none self-center bg-transparent py-2 text-[16px] leading-relaxed text-fg outline-none placeholder:text-faint"
        />
        <button
          type="button"
          onClick={submit}
          disabled={!canSend}
          aria-label={isSending ? "Sending" : "Send message"}
          className={cn(
            "flex size-9 shrink-0 items-center justify-center rounded-full transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent",
            canSend
              ? "bg-fg text-canvas hover:opacity-90"
              : "bg-fg/10 text-faint",
          )}
        >
          {isSending ? <Spinner className="size-4" /> : <ArrowUpIcon />}
        </button>
      </div>

      <div
        className={cn(
          "mt-2 flex justify-between px-3 text-[11px]",
          overLimit ? "text-danger" : "text-faint opacity-70",
        )}
      >
        <span>Enter to send &nbsp;·&nbsp; Shift+Enter for a new line</span>
        <span className="tabular-nums">{MAX_LENGTH - value.length}</span>
      </div>
    </div>
  )
}
