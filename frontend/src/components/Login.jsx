import { useState } from "react"
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
} from "firebase/auth"
import { auth } from "../firebase"

export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isSignup, setIsSignup] = useState(false)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")
    setLoading(true)
    try {
      if (isSignup) {
        await createUserWithEmailAndPassword(auth, email, password)
      } else {
        await signInWithEmailAndPassword(auth, email, password)
      }
    } catch (err) {
      setError(err.message.replace("Firebase: ", ""))
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
      <form onSubmit={handleSubmit} style={{
        width: 340,
        padding: "32px 28px",
        borderRadius: 16,
        background: "#2a2a2a",
        border: "1px solid #3a3a3a",
        display: "flex",
        flexDirection: "column",
        gap: 12,
      }}>
        <div style={{ textAlign: "center", fontSize: "32px" }}>🎓</div>
        <h1 style={{ color: "#ececec", fontSize: 20, margin: 0, textAlign: "center" }}>
          CampusGuideGPT
        </h1>
        <p style={{ color: "#8e8ea0", fontSize: 14, margin: "0 0 8px", textAlign: "center" }}>
          {isSignup ? "Create an account" : "Sign in to continue"}
        </p>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{
            padding: "12px 14px",
            borderRadius: 10,
            border: "1px solid #3f3f3f",
            background: "#2f2f2f",
            color: "#ececec",
            fontSize: 14,
            outline: "none",
          }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={6}
          style={{
            padding: "12px 14px",
            borderRadius: 10,
            border: "1px solid #3f3f3f",
            background: "#2f2f2f",
            color: "#ececec",
            fontSize: 14,
            outline: "none",
          }}
        />

        {error && <p style={{ color: "#ef4444", fontSize: 13, margin: 0 }}>{error}</p>}

        <button type="submit" disabled={loading} style={{
          padding: "12px 14px",
          borderRadius: 10,
          border: "none",
          background: loading ? "#3f3f3f" : "#ececec",
          color: loading ? "#8e8ea0" : "#212121",
          fontWeight: 600,
          fontSize: 14,
          cursor: loading ? "not-allowed" : "pointer",
          marginTop: 4,
          transition: "all 0.15s",
        }}>
          {loading ? "..." : isSignup ? "Sign up" : "Sign in"}
        </button>

        <p onClick={() => setIsSignup(!isSignup)} style={{
          color: "#8e8ea0",
          fontSize: 13,
          textAlign: "center",
          cursor: "pointer",
          marginTop: 4,
          textDecoration: "underline",
        }}>
          {isSignup ? "Already have an account? Sign in" : "No account? Sign up"}
        </p>
      </form>
    </div>
  )
}