# CampusGuideGPT — Frontend

React 19 + TypeScript (strict) + Vite + Tailwind CSS v4.
Design system: [`../DESIGN.md`](../DESIGN.md) · conventions: [`../guidelines.md`](../guidelines.md).

## Run

    npm install
    cp .env.example .env    # fill in the values
    npm run dev

Open the URL Vite prints (http://localhost:5173 by default).

## Scripts

- `npm run dev` — dev server
- `npm run build` — `tsc --noEmit` then production build
- `npm run typecheck` — types only
- `npm run lint` — ESLint (typescript-eslint, strict)

## Structure

    src/
    ├── components/
    │   ├── ui/          Button, IconButton, TextField, Spinner, TypingDots, icons
    │   └── chat/        ChatShell, Sidebar, Header, MessageList, Message, Composer, …
    │   └── auth/        Login, VerifyEmail
    ├── hooks/           useAuth, useChat, useConversations, useTheme,
    │                    useMediaQuery, useAutoScroll, useFocusTrap
    ├── lib/             cn, firebase, api (/ask), conversations (Firestore)
    ├── types/           chat
    ├── routes/          NotFound
    └── styles/          globals.css — design tokens + Tailwind

Chat history is persisted per user in Firestore under
`users/{uid}/conversations/{id}`. The `/ask` backend is non-streaming; the
composer awaits the full answer behind a typing indicator.
