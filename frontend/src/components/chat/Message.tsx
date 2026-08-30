import { memo, isValidElement, type ReactElement } from "react"
import ReactMarkdown, { type Components, type Options } from "react-markdown"
import remarkGfm from "remark-gfm"
import rehypeHighlight from "rehype-highlight"
import type { ChatMessage } from "../../types/chat"
import { TypingDots } from "../ui/TypingDots"
import { MessageSources } from "./MessageSources"

const remarkPlugins: Options["remarkPlugins"] = [remarkGfm]
const rehypePlugins: Options["rehypePlugins"] = [
  [rehypeHighlight, { detect: false, ignoreMissing: true }],
]

function langOf(child: unknown): string | undefined {
  if (!isValidElement(child)) return undefined
  const className = (child as ReactElement<{ className?: string }>).props.className ?? ""
  return /language-([\w-]+)/.exec(className)?.[1]
}

const components: Components = {
  a: (props) => <a {...props} target="_blank" rel="noreferrer noopener" />,
  table: (props) => (
    <div className="md-table-wrap">
      <table {...props} />
    </div>
  ),
  pre: ({ children, ...props }) => (
    <pre {...props} data-lang={langOf(Array.isArray(children) ? children[0] : children)}>
      {children}
    </pre>
  ),
}

/** Memoized so appending or editing another message never re-parses this one. */
const MarkdownBody = memo(function MarkdownBody({ content }: { content: string }) {
  return (
    <div className="message-markdown text-fg">
      <ReactMarkdown
        remarkPlugins={remarkPlugins}
        rehypePlugins={rehypePlugins}
        components={components}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
})

interface MessageProps {
  message: ChatMessage
}

export const Message = memo(function Message({ message }: MessageProps) {
  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] whitespace-pre-wrap rounded-3xl rounded-br-lg bg-bubble px-4 py-3 text-[16px] leading-relaxed text-fg">
          {message.content}
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-1.5">
      <span className="text-[13px] text-muted">CampusGuideGPT</span>

      {message.status === "pending" && message.content === "" ? (
        <TypingDots />
      ) : message.status === "error" ? (
        <p className="text-[16px] leading-relaxed text-danger">{message.content}</p>
      ) : (
        <MarkdownBody content={message.content} />
      )}

      {message.sources && message.sources.length > 0 && <MessageSources sources={message.sources} />}
    </div>
  )
})
