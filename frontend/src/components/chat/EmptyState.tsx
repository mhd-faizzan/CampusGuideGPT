function greeting(): string {
  const h = new Date().getHours()
  if (h < 12) return "Good morning"
  if (h < 18) return "Good afternoon"
  return "Good evening"
}

interface EmptyStateProps {
  name?: string
}

export function EmptyState({ name }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center gap-2 text-center">
      <h1 className="font-serif text-[28px] text-fg">
        {greeting()}
        {name ? `, ${name}` : ""}
      </h1>
      <p className="text-sm text-muted">your AI guide for Hochschule Harz</p>
    </div>
  )
}
