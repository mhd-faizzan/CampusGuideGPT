import { useState } from "react"
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendEmailVerification,
  updateProfile,
} from "firebase/auth"
import { doc, setDoc } from "firebase/firestore"
import { auth, db } from "../firebase"

export default function Login() {
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [isHHStudent, setIsHHStudent] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [isSignup, setIsSignup] = useState(false)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  const [focused, setFocused] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")

    if (isSignup && !isHHStudent) {
      setError("please select an option")
      return
    }

    setLoading(true)
    try {
      if (isSignup) {
        const cred = await createUserWithEmailAndPassword(auth, email, password)
        await updateProfile(cred.user, { displayName: `${firstName} ${lastName}` })
        await setDoc(doc(db, "users", cred.user.uid), {
          firstName,
          lastName,
          email,
          isHHStudent,
          createdAt: new Date().toISOString(),
        })
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
    width: "100%",
  })

  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      height: "100vh",
      background: "#212121",
      padding: 20,
    }}>
      <form onSubmit={handleSubmit} style={{
        width: 380,
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

        {isSignup && (
          <div style={{ display: "flex", gap: 10 }}>
            <input
              type="text"
              placeholder="First name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              onFocus={() => setFocused("firstName")}
              onBlur={() => setFocused("")}
              required
              style={inputStyle("firstName")}
            />
            <input
              type="text"
              placeholder="Last name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              onFocus={() => setFocused("lastName")}
              onBlur={() => setFocused("")}
              required
              style={inputStyle("lastName")}
            />
          </div>
        )}

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

        <div style={{ position: "relative" }}>
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onFocus={() => setFocused("password")}
            onBlur={() => setFocused("")}
            required
            minLength={6}
            style={{ ...inputStyle("password"), paddingRight: 44 }}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            style={{
              position: "absolute", right: 12, top: "50%", transform: "translateY(-50%)",
              background: "none", border: "none", color: "#8e8ea0", cursor: "pointer", fontSize: 13,
            }}
          >
            {showPassword ? "hide" : "show"}
          </button>
        </div>

        {isSignup && (
          <select
            value={isHHStudent}
            onChange={(e) => setIsHHStudent(e.target.value)}
            required
            style={{ ...inputStyle("hh"), color: isHHStudent ? "#ececec" : "#8e8ea0" }}
          >
            <option value="" disabled>Are you a student at Hochschule Harz?</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        )}

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
        }}>
          {loading ? "..." : isSignup ? "Sign up" : "Sign in"}
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
      </form>
    </div>
  )
}