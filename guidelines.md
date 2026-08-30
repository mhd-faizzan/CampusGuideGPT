# CampusGuideGPT — Frontend Guidelines

Architecture and coding rules for the UI rebuild. Pairs with `DESIGN.md`
(visual system — the source of truth for anything visual). Scope: `frontend/`.
The backend (`/ask`, FastAPI) is unchanged and non-streaming.

## Stack (pinned)

| Layer | Choice | Notes |
|---|---|---|
| Language | **TypeScript 5.9** (`~5.9`), strict | *not* 7.x — `typescript-eslint` peer caps at `<6.1` |
| Framework | React 19.2 | built-in state only |
| Build | Vite 8 | `@vitejs/plugin-react` + `@tailwindcss/vite` |
| Styling | Tailwind CSS v4 | tokens via `@theme inline`, no `tailwind.config` |
| Class utils | `clsx` + `tailwind-merge` | exported as `cn()` from `src/lib/cn.ts` |
| Variants | `class-variance-authority` | for `Button` and any multi-variant primitive |
| Routing | `react-router-dom` 6 | routes unchanged (`/`, `*`) |
| Auth / DB | `firebase` 12 | Auth + Firestore, as today |
| Markdown | `react-markdown` | assistant messages |
| Lint | `eslint` + `typescript-eslint` recommended | `no-explicit-any` stays on |

**Not adopted** (deliberately, for an app this size): Zustand, TanStack Query,
React Hook Form, Zod, shadcn/ui CLI, Radix, Playwright, **SSE / token streaming**.
Revisit only with a concrete need.

## TypeScript

```jsonc
// tsconfig.json compilerOptions (strict baseline)
"strict": true,
"noUncheckedIndexedAccess": true,
"noImplicitOverride": true,
"noUnusedLocals": true,
"noUnusedParameters": true,
"verbatimModuleSyntax": true,   // use `import type { X }` for type-only imports
"moduleResolution": "bundler",
"module": "ESNext",
"target": "ES2022",
"jsx": "react-jsx",
"noEmit": true                  // Vite builds; `tsc --noEmit` is the typecheck
```

- **No `any`.** Use `unknown` + narrowing at boundaries (fetch responses,
  Firestore snapshots, caught errors).
- `import.meta.env` is typed in `src/vite-env.d.ts` (`VITE_API_URL`,
  `VITE_FIREBASE_*`).
- `npm run build` = `tsc --noEmit && vite build`. `npm run typecheck` = `tsc --noEmit`.

## Directory structure

```
frontend/src/
├── main.tsx                 # Router mount
├── App.tsx                  # auth gate → chat shell
├── routes/
│   └── NotFound.tsx
├── components/
│   ├── ui/                  # primitives: Button, IconButton, TextField, Spinner, TypingDots
│   ├── chat/                # Sidebar, SidebarItem, Header, EmptyState,
│   │                        #   MessageList, Message, MessageSources, Composer
│   └── auth/                # Login, VerifyEmail
├── hooks/                   # useAuth, useConversations, useChat, useAutoScroll,
│                            #   useMediaQuery, useTheme, useFocusTrap
├── lib/
│   ├── cn.ts                # clsx + tailwind-merge
│   ├── firebase.ts
│   ├── api.ts               # ask(question, token, signal?) -> Promise<{ answer, sources }>
│   └── conversations.ts     # Firestore CRUD (typed port of current conversations.js)
├── types/
│   └── chat.ts              # Role, Source, ChatMessage, Conversation
└── styles/
    └── globals.css          # @import "tailwindcss"; token blocks; base; .message-markdown; keyframes
```

## Naming

- Components `PascalCase`, one component per file, filename = component name.
- Props `camelCase`. Boolean props prefixed `is` / `has` / `should`
  (`isLoading`, `isDisabled`, `hasError`).
- Hooks `useX`. Event handlers `handleX` inside components, `onX` as props.
- Types/interfaces `PascalCase`; no `I` prefix.

## Component API conventions

- **Composition over configuration.** Prefer `<Card><CardHeader/>…</Card>` shapes
  over one component with 15 props.
- **Props over `className` overrides.** Only `ui/` primitives accept a
  `className` passthrough, merged with `cn()`. Feature components do not take an
  arbitrary `className`.
- Multi-variant primitives define variants with **CVA**; no ad-hoc conditional
  class strings for variant logic.
- Controlled inputs: `value` + `onChange`. Select-like primitives:
  `value` + `onValueChange` + optional `defaultValue`.
- Icon-only interactive elements **must** have an accessible name — enforced via
  the `IconButton` primitive (required `aria-label` prop).

## Styling rules

- Tailwind utilities with **token classes only** for color
  (`bg-surface`, `text-secondary`, `border-border-subtle`, `ring-accent`,
  `text-accent`). No raw hex, no arbitrary color values in JSX.
- Non-color arbitrary values are fine where no token exists
  (`max-w-[768px]`, `min-h-[44px]`).
- Spacing between siblings via parent `flex`/`grid` + `gap`. Avoid `mt-*`/`mb-*`
  on children to create rhythm.
- **Accent (`--accent`) is used only for links and `:focus-visible` rings** — per
  DESIGN.md, never as a button fill or surface in the chat area. Primary button =
  `text-primary` background on `bg` text (Claude-style neutral). Secondary =
  `surface` + subtle ring. Ghost = transparent, hover `surface`.
- Body copy is **16px / 1.65–1.75**; UI text 14px; meta 13px; micro 11px.
- `globals.css` owns only: `@import "tailwindcss"`, the token blocks, `body`
  base, `.message-markdown` typography, keyframes (`typing-bounce`), and
  `prefers-reduced-motion` overrides. Nothing else.

### Theme token blocks (dark-first)

```css
:root {                      /* DARK is the base palette */
  --background: #0d0d0d; --sidebar:#171717; --surface:#212121; …
  --accent:#5b8def; --danger:#ef4444;
}
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) { /* …light values… */ }
}
[data-theme="light"] { /* …light values (wins over media query)… */ }
[data-theme="dark"]  { /* …dark values (re-assert for explicit choice)… */ }
```

- Every color has a value on bare `:root` (dark).
- `useTheme()` toggles `data-theme` on `<html>` and persists the choice in
  `localStorage`; default (unset) follows the OS.
- Expose tokens to Tailwind with `@theme inline` (`--color-surface: var(--surface)` …).

## State & data

- **React built-ins only**: `useState`, `useReducer`, `useContext`. No external
  store.
- Firebase listeners live in hooks and return their unsubscribe from `useEffect`.
  `useAuth()` → `{ user, loading }`. `useConversations(uid)` → live list.
- `useChat()` owns the message array + `sendMessage(text)` and calls
  `lib/api.ask` then `lib/conversations.appendTurn` on a completed turn. There is
  **no `stop()`** — the request is awaited behind a typing indicator; the
  composer and sidebar disable while it's pending.
- Behaviour to preserve from commit `77e2a8b`:
  - conversation doc created lazily on first successful answer;
  - greeting bubble and error / rate-limit replies are **not** persisted;
  - conversation switching / creation disabled while a request is in flight.
- `lib/api.ask` throws a typed `ApiError(status, message)` for non-2xx; callers
  map 429 / 500 / network failure to a visible assistant error message
  (`danger` text).

## Accessibility (target: WCAG 2.2 AA)

- All text meets 4.5:1 contrast in both themes; large text 3:1.
- Message list container: `role="log"` + `aria-live="polite"` so new answers are
  announced.
- Visible `:focus-visible` ring (2px `accent`) on interactive elements only —
  never a focus rectangle on a scroll container or layout wrapper.
- Touch targets ≥ 44×44px.
- Mobile drawer: focus trap while open, `Esc` closes, focus returns to the
  toggle. `aria-expanded` on the toggle.
- Composer textarea has a visually-hidden label. Send button label reflects
  state (`Send` / `Sending…`).
- Respect `prefers-reduced-motion`: no sidebar slide, no typing bounce.

## Migration approach

1. Rebuild **in place on `ver1.1`**, converting `.jsx` → `.tsx`. Restore point:
   `77e2a8b`.
2. Order: tooling (tsconfig, Tailwind v4, `cn`, token blocks) → `types/` +
   `lib/` (port firebase / api / conversations, typed) → `ui/` primitives →
   `chat/` + `auth/` features → `App.tsx` + routing → delete old `.jsx`.
3. Keep the backend contract identical: `POST /ask` with Bearer token →
   `{ answer, sources }`; 400 / 429 / 500 JSON `{ error }`.
4. Every step leaves `npm run typecheck`, `npm run lint`, `npm run build` green.
5. No commits without an explicit ask; commit per logical step when asked.

## Definition of done

- `typecheck`, `lint`, `build` clean; zero `any`.
- Light and dark both correct, including OS-default (no `data-theme`) and the
  manual toggle; no wrong-theme flash on load.
- No hard 1px structural borders anywhere (sidebar / header / main).
- Assistant messages have no background bubble; accent appears only on links and
  focus rings.
- Sidebar collapses to 0 with a smooth transition, no residual line, main column
  reflows to full width with no layout jump.
- Mobile: sidebar drawer traps focus, closes on `Esc` and scrim tap; safe-area
  insets respected.
- Ask → typing indicator → answer → appears in sidebar → survives reload →
  reopen works. 429 / 500 / offline render as a `danger` assistant message.
- Keyboard-only pass: every action reachable, focus always visible, no focus
  rectangles on containers.
