import { forwardRef, useId, type InputHTMLAttributes, type ReactNode } from "react"
import { cn } from "../../lib/cn"

export interface TextFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string
  hideLabel?: boolean
  error?: string
  trailing?: ReactNode
}

export const TextField = forwardRef<HTMLInputElement, TextFieldProps>(function TextField(
  { label, hideLabel = false, error, trailing, className, id, ...props },
  ref,
) {
  const autoId = useId()
  const fieldId = id ?? autoId
  const errorId = `${fieldId}-error`

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={fieldId} className={cn("text-sm text-muted", hideLabel && "sr-only")}>
        {label}
      </label>
      <div className="relative">
        <input
          ref={ref}
          id={fieldId}
          aria-invalid={error ? true : undefined}
          aria-describedby={error ? errorId : undefined}
          className={cn(
            "w-full rounded-xl bg-surface px-3.5 py-3 text-[15px] text-fg outline-none ring-1 ring-inset ring-subtle transition-shadow placeholder:text-faint focus-visible:ring-2 focus-visible:ring-accent",
            trailing && "pr-11",
            error && "ring-danger",
            className,
          )}
          {...props}
        />
        {trailing && <div className="absolute inset-y-0 right-2 flex items-center">{trailing}</div>}
      </div>
      {error && (
        <p id={errorId} className="text-[13px] text-danger">
          {error}
        </p>
      )}
    </div>
  )
})
