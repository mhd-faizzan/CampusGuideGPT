import { useState } from "react"
import { sendEmailVerification, signOut } from "firebase/auth"
import { auth } from "../firebase"

export default function VerifyEmail() {
  const [sent, setSent] = useState(false)
  const [loading, setLoading] = useState(false)

  const resend = async () => {
    setLoading(true)
    try {
      await sendEmailVerification(auth.currentUser)
      setSent(true)
    } catch {
      // rate limited by firebase, fine to ignore
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      height: "100vh",
      background: "#212121",
    }}>
      <div style={{
        width: 360,
        padding: "36px 32px",
        borderRadius: 16,
        background: "#2a2a2a",
        border: "1px solid #3a3a3a",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 14,
        textAlign: "center",
      }}>
        <div style={{ fontSize: "34px" }}>📩</div>
        <h1 style={{ color: "#ececec", fontSize: 20, fontWeight: 600, margin: 0 }}>
          Verify your email
        </h1>
        <p style={{ color: "#8e8ea0", fontSize: 14, margin: 0 }}>
          We sent a verification link to <b style={{ color: "#ececec" }}>{auth.currentUser?.email}</b>.
          Click it, then refresh this page.
        </p>

        <button onClick={() => window.location.reload()} style={{
          width: "100%",
          padding: "12px 14px",
          borderRadius: 10,
          border: "none",
          background: "#ececec",
          color: "#212121",
          fontWeight: 600,
          fontSize: 14,
          cursor: "pointer",
          marginTop: 6,
        }}>
          I've verified, refresh
        </button>

        <button onClick={resend} disabled={loading || sent} style={{
          background: "none",
          border: "none",
          color: "#8e8ea0",
          fontSize: 13,
          cursor: loading || sent ? "default" : "pointer",
          textDecoration: sent ? "none" : "underline",
        }}>
          {sent ? "Verification email sent" : loading ? "Sending..." : "Resend email"}
        </button>

        <button onClick={() => signOut(auth)} style={{
          background: "none", border: "none", color: "#666", fontSize: 12, cursor: "pointer", marginTop: 8,
        }}>
          Sign out
        </button>
      </div>
    </div>
  )
}