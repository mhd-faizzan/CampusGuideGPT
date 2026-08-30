# DESIGN.md
## Claude-Style Chat Application
**Best-in-class modern UI system**
**Stack:** TypeScript (strict) + React 19 + Vite + Tailwind CSS
**Last updated:** August 30, 2026

---

## Overview

This document defines the complete visual and interaction design for a modern AI chat application.
The goal is to achieve the same level of calm, refined, and professional quality as Claude.ai while
remaining fully implementable with official tools only.

Core principles:
- Dark-first
- Extremely low visual noise
- Soft depth instead of hard borders
- Assistant messages have no bubble
- Composer feels floating and premium
- Excellent accessibility and keyboard support

---

## Color System

### Dark Mode (Default)
```css
:root {
  --background:          #0d0d0d;
  --sidebar:             #171717;
  --surface:             #212121;
  --composer-bg:         rgba(42, 42, 42, 0.80);
  --border-subtle:       rgba(255, 255, 255, 0.06);
  --text-primary:        #ffffff;
  --text-secondary:      rgba(255, 255, 255, 0.50);
  --text-tertiary:       rgba(255, 255, 255, 0.40);
  --user-bubble:         #2f2f2f;
  --accent:              #5b8def;          /* only for focus rings & links */
  --danger:              #ef4444;
}
```

### Light Mode
```css
[data-theme="light"] {
  --background:          #ffffff;
  --sidebar:             #f7f7f8;
  --surface:             #f4f4f5;
  --composer-bg:         rgba(255, 255, 255, 0.85);
  --border-subtle:       rgba(0, 0, 0, 0.06);
  --text-primary:        #0d0d0d;
  --text-secondary:      rgba(0, 0, 0, 0.55);
  --text-tertiary:       rgba(0, 0, 0, 0.40);
  --user-bubble:         #f4f4f5;
  --accent:              #2563eb;
}
```

Theme resolution order:
- `data-theme="dark"` → always dark
- `data-theme="light"` → always light
- Otherwise follow `prefers-color-scheme`

---

## Typography

- Font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif`
- Body text: 16px / 1.65–1.75 line-height
- Headings: tracking-tight, medium weight
- Secondary text: 50% opacity
- Tertiary text / disclaimers: 40% opacity
- Code: prefer system mono or JetBrains Mono

---

## Layout

### Desktop
- Sidebar: 260px expanded → fully collapsible (0px)
- Main message column: `max-width: 768px`, centered
- Composer: sticky bottom, floating
- No hard vertical or horizontal structural lines

### Mobile
- Sidebar becomes a drawer with proper focus trap
- Full-width messages
- Composer remains fully usable
- Safe-area insets respected

---

## Components

### 1. Sidebar
- Background: `var(--sidebar)`
- No `border-right`
- Smooth width transition (200–250ms)
- When collapsed, main content becomes full width

### 2. Header
- No bottom border
- Minimal height
- Actions aligned to the right

### 3. Message List
- Centered, `max-w-[768px]`
- Comfortable vertical rhythm (`gap-6`)
- Auto-scroll only when user is near the bottom

### 4. Messages
- Assistant: No background bubble, full width, clean markdown
- User: Soft bubble (`var(--user-bubble)`), `rounded-3xl`, max-width 85%, aligned right
- Pending reply: the last assistant message is a typing indicator (no bubble) until the answer arrives

### 5. Composer (Most Important)
```css
.composer {
  background: var(--composer-bg);
  backdrop-filter: blur(12px);
  border-radius: 1.75rem;
  border: none;
  box-shadow:
    0 0 0 1px var(--border-subtle),
    0 8px 30px rgba(0, 0, 0, 0.30);
}
```
- Auto-growing textarea
- Send button shows a loading state and is disabled while a reply is pending
- Enter = send, Shift+Enter = new line
- Clear focus states

### 6. Empty State
- Centered vertically
- Heading → subtitle spacing: 12px
- Subtitle → composer spacing: 32px
- Subtitle at 50% opacity
- Disclaimer at 40% opacity

---

## Interaction Rules

- Show the typing indicator immediately on send; swap it for the answer when it arrives
- Auto-scroll only when near bottom
- Focus trap required on mobile drawer
- Visible `:focus-visible` rings on interactive elements only
- No large focus rectangles on containers

---

## Accessibility Requirements

- All interactive elements have accessible names
- `role="log"` + `aria-live="polite"` on message list
- Keyboard navigation fully supported
- Escape closes drawer
- Color contrast ≥ 4.5:1
- Touch targets ≥ 44×44px

---

## Do's and Don'ts

### Do
- Use soft shadows and background color differences
- Keep assistant messages bubble-free
- Make the composer feel floating and premium
- Prefer calm, neutral surfaces
- Maintain excellent keyboard and screen-reader support

### Don't
- Add hard 1px structural borders
- Give assistant messages a background bubble
- Use strong colorful accents in the main chat area
- Make the interface busy or noisy
- Sacrifice accessibility for aesthetics

---

## Implementation Notes

- Use CSS variables for every color
- Prefer Tailwind utility classes + CSS variables
- Keep components small and focused
- Strict TypeScript only (`strict: true`, no `any`)
- Native Fetch for the `/ask` request (no extra libraries required)
- Token-by-token streaming is out of scope in this version — `/ask` returns the
  full answer in one response; the composer awaits it behind a typing indicator

---

_This is the single source of truth for visual design._
_All future UI work must follow this document._
