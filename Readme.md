# CampusGuideGPT

> AI assistant for Hochschule Harz students — ask anything about admissions, campus life, programs, or accommodation.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React-61dafb)
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
4. passing those answers + your question to an LLM (Llama 3.3 70B via Groq)
5. returning a clean, conversational response

This approach is called RAG — the model doesn't just guess, it retrieves real context first.

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Backend | FastAPI + Python 3.11 | fast, modern, production-ready |
| Frontend | React + Vite | clean, fast, component-based |
| Embeddings | fastembed (all-MiniLM-L6-v2) | lightweight, no GPU needed |
| Vector DB | Pinecone | managed vector search |
| LLM | Llama 3.3 70B via Groq | fast inference, free tier |
| Deployment | Railway (backend) + Vercel (frontend) | free, auto-deploy from GitHub |

---

## Architecture

    Your Question
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
    Groq LLM — Llama 3.3 70B (generates answer)
         │
         ▼
    Response + Source References

---

## Project Structure

    CampusGuideGPT/
    ├── backend/
    │   ├── main.py                  # FastAPI app — all routes live here
    │   ├── Dockerfile               # for Railway deployment
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
    │       └── rate_tracker.py      # global daily usage counter
    └── frontend/
        ├── index.html
        ├── vite.config.js
        └── src/
            ├── App.jsx              # main app, handles API calls
            ├── main.jsx             # entry point, router setup
            ├── index.css            # global styles
            ├── NotFound.jsx         # 404 page
            └── components/
                ├── ChatWindow.jsx   # renders the chat messages
                ├── MessageBubble.jsx # single message with sources
                └── InputBar.jsx     # text input + send button

---

## Run Locally

You need: Python 3.11, Node.js 18+, a Pinecone account, and a Groq API key.

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

**3. run backend**

    cd backend
    uvicorn main:app --reload

backend is live at http://localhost:8000

**4. setup frontend**

open a new terminal:

    cd frontend
    npm install
    cp .env.example .env

open `frontend/.env` and set:

    VITE_API_URL=http://localhost:8000

**5. run frontend**

    npm run dev

open http://localhost:5173

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| /health | GET | none | server status check |
| /stats | GET | secret key | daily usage stats |
| /ask | POST | none | ask a question |

**ask a question:**

    POST /ask
    Content-Type: application/json

    { "question": "how do I register in Wernigerode?" }

**check stats:**

    GET /stats?secret=your-secret-key

---

## Deployment

**Backend → Railway**

1. connect GitHub repo on Railway
2. set root directory to `backend`
3. set builder to Dockerfile
4. add environment variables (same as `.env`)
5. generate a public domain

**Frontend → Vercel**

1. connect GitHub repo on Vercel
2. set root directory to `frontend`
3. add `VITE_API_URL` pointing to your Railway backend URL
4. deploy

Every push to `main` auto-deploys both services.

---

## Limitations

The knowledge base contains a limited, curated set of Q&A pairs manually indexed into Pinecone. It does not cover every aspect of Hochschule Harz or German university processes. For topics outside the knowledge base, the assistant falls back to general LLM knowledge which may not always be accurate. Always verify important information through official university channels.

---

## License

MIT