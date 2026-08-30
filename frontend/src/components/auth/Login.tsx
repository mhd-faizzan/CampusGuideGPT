import { useState, type FormEvent } from "react"
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendEmailVerification,
  sendPasswordResetEmail,
  updateProfile,
} from "firebase/auth"
import { doc, setDoc } from "firebase/firestore"
import { auth, db } from "../../lib/firebase"
import { Button } from "../ui/Button"
import { TextField } from "../ui/TextField"
import { CampusIcon } from "../ui/icons"

function errCode(err: unknown): string {
  if (typeof err === "object" && err !== null && "code" in err) {
    return String((err as { code: unknown }).code)
  }
  return ""
}

function friendlyError(code: string): string {
  switch (code) {
    case "auth/invalid-credential":
    case "auth/wrong-password":
    case "auth/user-not-found":
      return "Incorrect email or password"
    case "auth/email-already-in-use":
      return "An account with this email already exists"
    case "auth/weak-password":
      return "Password should be at least 6 characters"
    case "auth/invalid-email":
      return "Enter a valid email address"
    case "auth/too-many-requests":
      return "Too many attempts. Try again in a bit"
    default:
      return "Something went wrong. Please try again"
  }
}

export function Login() {
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [isHHStudent, setIsHHStudent] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [isSignup, setIsSignup] = useState(false)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  const [resetSent, setResetSent] = useState(false)

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError("")

    if (isSignup && !isHHStudent) {
      setError("Please select whether you're a Hochschule Harz student")
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
      setError(friendlyError(errCode(err)))
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async () => {
    if (!email) {
      setError("Enter your email first, then tap “Forgot password?”")
      return
    }
    setError("")
    try {
      await sendPasswordResetEmail(auth, email)
      setResetSent(true)
    } catch (err) {
      setError(friendlyError(errCode(err)))
    }
  }

  return (
    <div className="flex min-h-dvh flex-col items-center justify-center bg-canvas px-5 py-12">
      <div className="mb-7 flex flex-col items-center gap-2.5">
        <CampusIcon className="size-7 text-fg" />
        <span className="text-[17px] font-semibold tracking-tight text-fg">CampusGuideGPT</span>
      </div>

      <form
        onSubmit={handleSubmit}
        className="flex w-full max-w-[400px] flex-col gap-4 rounded-[1.5rem] bg-sidebar p-8 sm:p-9"
        style={{
          boxShadow: "0 0 0 1px var(--border-subtle), 0 16px 50px -12px rgba(0, 0, 0, 0.28)",
        }}
      >
        <div className="mb-1 flex flex-col gap-1.5 text-center">
          <h1 className="text-[24px] font-semibold tracking-tight text-fg">
            {isSignup ? "Create your account" : "Welcome back"}
          </h1>
          <p className="text-[15px] text-muted">
            {isSignup
              ? "Sign up to start using CampusGuideGPT"
              : "Sign in to CampusGuideGPT to continue"}
          </p>
        </div>

        {isSignup && (
          <div className="flex gap-3">
            <TextField
              label="First name"
              hideLabel
              placeholder="First name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
            <TextField
              label="Last name"
              hideLabel
              placeholder="Last name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>
        )}

        <TextField
          label="Email address"
          hideLabel
          type="email"
          placeholder="Email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <div className="flex flex-col gap-1.5">
          <TextField
            label="Password"
            hideLabel
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
            trailing={
              <button
                type="button"
                onClick={() => setShowPassword((v) => !v)}
                className="rounded px-2 py-1 text-[13px] text-muted transition-colors hover:text-fg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            }
          />
          {!isSignup && (
            <button
              type="button"
              onClick={handleReset}
              className="self-end rounded text-[13px] text-muted transition-colors hover:text-fg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
            >
              {resetSent ? "Reset email sent — check your inbox" : "Forgot password?"}
            </button>
          )}
        </div>

        {isSignup && (
          <div className="flex flex-col gap-1.5">
            <label htmlFor="hh-student" className="text-sm text-muted">
              Are you a student at Hochschule Harz?
            </label>
            <select
              id="hh-student"
              value={isHHStudent}
              onChange={(e) => setIsHHStudent(e.target.value)}
              required
              className="w-full rounded-xl bg-surface px-3.5 py-3 text-[15px] text-fg outline-none ring-1 ring-inset ring-subtle transition-shadow focus-visible:ring-2 focus-visible:ring-accent"
            >
              <option value="" disabled>
                Select an option
              </option>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </div>
        )}

        {error && (
          <p role="alert" className="rounded-xl bg-danger/10 px-3.5 py-2.5 text-[13px] text-danger">
            {error}
          </p>
        )}

        <Button type="submit" isLoading={loading} className="mt-1 w-full">
          {isSignup ? "Sign up" : "Sign in"}
        </Button>

        <button
          type="button"
          onClick={() => {
            setIsSignup((v) => !v)
            setError("")
            setResetSent(false)
          }}
          className="rounded text-center text-[13px] text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
        >
          {isSignup ? "Already have an account? " : "Don't have an account? "}
          <span className="font-medium text-fg">{isSignup ? "Sign in" : "Sign up"}</span>
        </button>
      </form>
    </div>
  )
}
