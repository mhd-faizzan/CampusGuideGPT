export default function NotFound() {
  return (
    <div className="flex min-h-dvh flex-col items-center justify-center gap-4 bg-canvas px-6 text-center">
      <div className="text-5xl" aria-hidden>
        🎓
      </div>
      <h1 className="text-[22px] font-semibold tracking-tight text-fg">Page not found</h1>
      <p className="text-sm text-muted">This page doesn't exist.</p>
      <a
        href="/"
        className="rounded text-sm text-accent underline underline-offset-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      >
        Go back home
      </a>
    </div>
  )
}
