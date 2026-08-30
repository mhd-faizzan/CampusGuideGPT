import { useState } from "react"
import type { Source } from "../../types/chat"
import { ChevronRightIcon } from "../ui/icons"

interface MessageSourcesProps {
  sources: Source[]
}

export function MessageSources({ sources }: MessageSourcesProps) {
  const [open, setOpen] = useState(false)
  if (sources.length === 0) return null

  return (
    <div className="mt-2">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="group -ml-1 inline-flex items-center gap-1 rounded-md px-1 py-0.5 text-[13px] text-faint transition-colors hover:text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      >
        <ChevronRightIcon
          className={`transition-transform duration-150 ${open ? "rotate-90" : ""}`}
        />
        {sources.length} source{sources.length === 1 ? "" : "s"}
      </button>

      {open && (
        <ul className="mt-1.5 flex flex-col gap-1 border-l border-subtle pl-3">
          {sources.map((source, i) => (
            <li key={i} className="py-0.5 text-[13px] leading-relaxed text-muted">
              <span className="mr-2 text-faint tabular-nums">{Math.round(source.score * 100)}%</span>
              {source.question}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
