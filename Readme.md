# CampusGuideGPT

> AI assistant for Hochschule Harz students — ask anything about admissions, campus life, programs, or accommodation.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178c6)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

**Live demo:** https://campus-guide-gpt.vercel.app

---

## What is this?

CampusGuideGPT is a RAG-based (Retrieval-Augmented Generation) AI chatbot built for Hochschule Harz students. Instead of searching through static FAQs or long university websites, you just ask a question in plain language and get a conversational answer.

It works by:
1. taking your question
2. converting it into a vector (a mathematical representation)
3. searching a knowledge base in Pinecone for the most relevant answers
4. passing those answers + your question to an LLM (GPT-OSS 120B via Groq)
5. returning a clean, conversational response

This approach is called RAG — the model doesn't just guess, it retrieves real context first.

You sign in with your email (Firebase Auth), and every conversation is saved to your
account in Firestore, so you can reopen an old chat and keep going.

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Backend | FastAPI + Python 3.11 | fast, modern, production-ready |
| Frontend | React 19 + TypeScript + Vite + Tailwind | typed, fast, component-based |
| Auth & storage | Firebase (Auth + Firestore) | email login + saved chat history |
| Embeddings | fastembed (all-MiniLM-L6-v2) | lightweight, no GPU needed |
| Vector DB | Pinecone | managed vector search |
| LLM | GPT-OSS 120B via Groq | fast inference, free tier |
| Deployment | Google Cloud Run (backend) + Vercel (frontend) | container backend, auto-deploy frontend |

---

## Architecture

    Your Question
         │
         ▼
    Firebase Auth (verifies your login token)
         │
         ▼
    Input Sanitizer (blocks prompt injection)
         │
         ▼
    Embedding Model (converts text → vector)
         │
         ▼
    Pinecone Vector Search (finds top 3 matching Q&A pairs)
         │
         ▼
    Prompt Builder (combines context + instructions)
         │
         ▼
    Groq LLM — GPT-OSS 120B (generates answer)
         │
         ▼
    Response + Source References  (+ saved to your chat history)

---

## Project Structure

    CampusGuideGPT/
    ├── backend/
    │   ├── main.py                  # FastAPI app — all routes live here
    │   ├── Dockerfile               # container image for Cloud Run
    │   ├── requirements.txt         # pinned dependencies
    │   ├── .env.example             # copy this to .env and fill in your keys
    │   ├── config/
    │   │   └── settings.py          # loads all config from .env
    │   ├── services/
    │   │   ├── embedding.py         # converts text to vectors
    │   │   ├── vector_db.py         # talks to Pinecone
    │   │   └── llm_service.py       # talks to Groq API
    │   └── utils/
    │       ├── prompt_builder.py    # builds the prompt with context
    │       ├── sanitizer.py         # blocks prompt injection attacks
    │       ├── firebase_auth.py     # verifies the Firebase ID token on /ask
    │       └── rate_tracker.py      # global daily usage counter
    └── frontend/
        ├── index.html
        ├── vite.config.ts
        └── src/
            ├── App.tsx              # auth gate → chat
            ├── main.tsx             # entry point, router setup
            ├── lib/
            │   ├── firebase.ts      # firebase init (auth + firestore)
            │   ├── api.ts           # calls POST /ask
            │   └── conversations.ts # saves / loads chats in firestore
            ├── hooks/               # useAuth, useChat, useConversations, useTheme, …
            ├── components/
            │   ├── chat/            # ChatShell, Sidebar, Header, MessageList, Message, Composer
            │   ├── auth/            # Login, VerifyEmail
            │   └── ui/              # Button, IconButton, TextField, icons, …
            ├── types/chat.ts        # shared types
            ├── routes/NotFound.tsx  # 404 page
            └── styles/globals.css   # design tokens + tailwind

---

## Run Locally

You need: Python 3.11, Node.js 18+, a Pinecone account, a Groq API key, and a Firebase
project (Email/Password sign-in + Firestore enabled).

**1. clone the repo**

    git clone https://github.com/mhd-faizzan/CampusGuideGPT.git
    cd CampusGuideGPT

**2. setup backend**

    uv venv --python 3.11
    source .venv/bin/activate
    uv pip install -r backend/requirements.txt
    cp backend/.env.example backend/.env

open `backend/.env` and fill in your keys:

    PINECONE_API_KEY=your-pinecone-api-key
    PINECONE_INDEX=your-index-name
    PINECONE_HOST=your-pinecone-host-url
    GROQ_API_KEY=your-groq-api-key
    DAILY_LIMIT=100
    ALLOWED_ORIGINS=http://localhost:5173
    FIREBASE_SERVICE_ACCOUNT=your-firebase-service-account-json

for local dev you can skip `FIREBASE_SERVICE_ACCOUNT` and instead drop the service
account file at `backend/firebase-key.json` (gitignored) — the app picks it up
automatically.

**3. run backend**

    cd backend
    uvicorn main:app --reload

backend is live at http://localhost:8000

**4. setup frontend**

open a new terminal:

    cd frontend
    npm install
    cp .env.example .env

open `frontend/.env` and set your backend URL + Firebase web config:

    VITE_API_URL=http://localhost:8000

    VITE_FIREBASE_API_KEY=your-firebase-web-api-key
    VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
    VITE_FIREBASE_PROJECT_ID=your-project-id
    VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
    VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
    VITE_FIREBASE_APP_ID=your-app-id

**5. run frontend**

    npm run dev

open http://localhost:5173

> **note:** for chat history to save, add a Firestore rule so a user can only
> touch their own data:
>
>     match /users/{uid}/{document=**} {
>       allow read, write: if request.auth != null && request.auth.uid == uid;
>     }

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| /health | GET | none | server status check |
| /stats | GET | secret key | daily usage stats |
| /ask | POST | Firebase ID token | ask a question |

**ask a question:** (the token comes from the signed-in frontend user)

    POST /ask
    Content-Type: application/json
    Authorization: Bearer <firebase-id-token>

    { "question": "how do I register in Wernigerode?" }

**check stats:**

    GET /stats?secret=your-secret-key

---

## Deployment

**Backend → Google Cloud Run**

1. build the image from `backend/Dockerfile` and push it to Artifact Registry
   (or connect the GitHub repo for continuous deploys)
2. deploy the service, pointing the source at `backend`
3. add environment variables (same as `.env`)
4. Cloud Run hands you a public `*.run.app` HTTPS URL

**Frontend → Vercel**

1. connect GitHub repo on Vercel
2. set root directory to `frontend`
3. add `VITE_API_URL` (your Cloud Run backend URL) + the `VITE_FIREBASE_*` vars
4. deploy

Vercel auto-deploys the frontend on every push to `main`; wire up Cloud Run's GitHub
trigger if you want the backend to do the same.

---

## Limitations

The knowledge base contains a limited, curated set of Q&A pairs manually indexed into Pinecone. It does not cover every aspect of Hochschule Harz or German university processes. For topics outside the knowledge base, the assistant falls back to general LLM knowledge which may not always be accurate. Always verify important information through official university channels.

---

## License

MIT