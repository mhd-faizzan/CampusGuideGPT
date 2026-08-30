import { useState } from "react"
import { sendEmailVerification, signOut } from "firebase/auth"
import { auth } from "../../lib/firebase"
import { Button } from "../ui/Button"

export function VerifyEmail() {
  const [sent, setSent] = useState(false)
  const [loading, setLoading] = useState(false)

  const resend = async () => {
    const current = auth.currentUser
    if (!current) return
    setLoading(true)
    try {
      await sendEmailVerification(current)
      setSent(true)
    } catch {
      // firebase rate-limits resends — safe to ignore
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-dvh items-center justify-center bg-canvas p-5">
      <div
        className="flex w-full max-w-[360px] flex-col items-center gap-3.5 rounded-2xl bg-surface p-8 text-center"
        style={{ boxShadow: "0 0 0 1px var(--border-subtle), 0 8px 30px rgba(0,0,0,0.20)" }}
      >
        <div className="text-[34px]" aria-hidden>
          📩
        </div>
        <h1 className="text-xl font-semibold tracking-tight text-fg">Verify your email</h1>
        <p className="text-sm text-muted">
          We sent a verification link to{" "}
          <span className="text-fg">{auth.currentUser?.email}</span>. Click it, then refresh this
          page.
        </p>

        <Button className="w-full" onClick={() => window.location.reload()}>
          I've verified, refresh
        </Button>

        <button
          type="button"
          onClick={resend}
          disabled={loading || sent}
          className="rounded text-[13px] text-muted underline underline-offset-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:no-underline disabled:opacity-70"
        >
          {sent ? "Verification email sent" : loading ? "Sending…" : "Resend email"}
        </button>

        <button
          type="button"
          onClick={() => void signOut(auth)}
          className="rounded text-xs text-faint focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
        >
          Sign out
        </button>
      </div>
    </div>
  )
}
