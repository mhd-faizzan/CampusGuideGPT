import { useAuth } from "./hooks/useAuth"
import { Login } from "./components/auth/Login"
import { VerifyEmail } from "./components/auth/VerifyEmail"
import { ChatShell } from "./components/chat/ChatShell"

export default function App() {
  const { user, loading } = useAuth()

  if (loading) return null
  if (!user) return <Login />
  if (!user.emailVerified) return <VerifyEmail />

  // key by uid so all chat state resets cleanly on account switch
  return <ChatShell key={user.uid} user={user} />
}
