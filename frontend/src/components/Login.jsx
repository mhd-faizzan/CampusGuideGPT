import { useState } from "react"
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendEmailVerification,
} from "firebase/auth"
import { auth } from "../firebase"

export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isSignup, setIsSignup] = useState(false)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  const [focused, setFocused] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")
    setLoading(true)
    try {
      if (isSignup) {
        const cred = await createUserWithEmailAndPassword(auth, email, password)
        await sendEmailVerification(cred.user)
      } else {
        await signInWithEmailAndPassword(auth, email, password)
      }
    } catch (err) {
      setError(err.message.replace("Firebase: ", ""))
    } finally {
      setLoading(false)
    }
  }

  const inputStyle = (name) => ({
    padding: "12px 14px",
    borderRadius: 10,
    border: `1px solid ${focused === name ? "#ececec" : "#3f3f3f"}`,
    background: "#2f2f2f",
    color: "#ececec",
    fontSize: 14,
    outline: "none",
    transition: "border 0.15s",
  })

  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      height: "100vh",
      background: "#212121",
    }}>
      <form onSubmit={handleSubmit} style={{
        width: 360,
        padding: "36px 32px",
        borderRadius: 16,
        background: "#2a2a2a",
        border: "1px solid #3a3a3a",
        display: "flex",
        flexDirection: "column",
        gap: 14,
      }}>
        <div style={{ textAlign: "center", fontSize: "34px", marginBottom: 4 }}>🎓</div>
        <h1 style={{ color: "#ececec", fontSize: 21, fontWeight: 600, margin: 0, textAlign: "center" }}>
          CampusGuideGPT
        </h1>
        <p style={{ color: "#8e8ea0", fontSize: 14, margin: "0 0 10px", textAlign: "center" }}>
          {isSignup ? "Create an account to get started" : "Sign in to continue"}
        </p>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          onFocus={() => setFocused("email")}
          onBlur={() => setFocused("")}
          required
          style={inputStyle("email")}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onFocus={() => setFocused("password")}
          onBlur={() => setFocused("")}
          required
          minLength={6}
          style={inputStyle("password")}
        />

        {error && (
          <div style={{
            background: "rgba(239,68,68,0.1)",
            border: "1px solid rgba(239,68,68,0.3)",
            borderRadius: 8,
            padding: "8px 12px",
            color: "#ef4444",
            fontSize: 13,
          }}>
            {error}
          </div>
        )}

        <button type="submit" disabled={loading} style={{
          padding: "12px 14px",
          borderRadius: 10,
          border: "none",
          background: loading ? "#3f3f3f" : "#ececec",
          color: loading ? "#8e8ea0" : "#212121",
          fontWeight: 600,
          fontSize: 14,
          cursor: loading ? "not-allowed" : "pointer",
          marginTop: 6,
          transition: "all 0.15s",
        }}>
          {loading ? (
            <span style={{
              display: "inline-block", width: 14, height: 14,
              border: "2px solid #8e8ea0", borderTopColor: "transparent",
              borderRadius: "50%", animation: "spin 0.6s linear infinite",
            }} />
          ) : isSignup ? "Sign up" : "Sign in"}
        </button>

        <p onClick={() => { setIsSignup(!isSignup); setError("") }} style={{
          color: "#8e8ea0",
          fontSize: 13,
          textAlign: "center",
          cursor: "pointer",
          marginTop: 6,
        }}>
          {isSignup ? "Already have an account? " : "No account? "}
          <span style={{ color: "#ececec", textDecoration: "underline" }}>
            {isSignup ? "Sign in" : "Sign up"}
          </span>
        </p>

        <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
      </form>
    </div>
  )
}