import { useState } from "react"
import type { Source } from "../../types/chat"

interface MessageSourcesProps {
  sources: Source[]
}

export function MessageSources({ sources }: MessageSourcesProps) {
  const [open, setOpen] = useState(false)
  if (sources.length === 0) return null

  return (
    <div className="mt-1">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="rounded text-[13px] text-muted underline underline-offset-2 transition-colors hover:text-fg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      >
        {open ? "Hide sources" : `${sources.length} source${sources.length === 1 ? "" : "s"}`}
      </button>

      {open && (
        <ul className="mt-2 flex flex-col gap-1.5">
          {sources.map((source, i) => (
            <li key={i} className="rounded-lg bg-surface px-3.5 py-2.5 text-[13px] text-muted">
              <div className="mb-1 font-medium text-fg">{Math.round(source.score * 100)}% match</div>
              {source.question}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
