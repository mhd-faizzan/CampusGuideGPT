# CampusGuideGPT

A RAG-based conversational AI assistant for Hochschule Harz students, built to answer questions about university applications, campus life, accommodation, and academic programs.

---

## Overview

CampusGuideGPT combines semantic vector search with a large language model to retrieve contextually relevant answers from a curated knowledge base. Rather than relying on static FAQs, it understands natural language questions and responds in a conversational, helpful tone.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Interface | Streamlit |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | Pinecone |
| LLM | Llama 3.3 70B via Groq API |
| Language | Python 3.11+ |

---

## Architecture

```
User Query
    │
    ▼
Embedding Model (all-MiniLM-L6-v2)
    │
    ▼
Pinecone Vector Search (top-k=3, namespace=ns1)
    │
    ▼
Prompt Builder (context + instructions)
    │
    ▼
Groq LLM (Llama 3.3 70B)
    │
    ▼
Structured Response + Source References
```

---

## Project Structure

```
CampusGuideGPT/
├── app.py
├── requirements.txt
├── config/
│   └── settings.py
├── services/
│   ├── embedding.py
│   ├── vector_db.py
│   └── llm_service.py
├── utils/
│   └── prompt_builder.py
└── ui/
    ├── styles.py
    └── components.py
```

---

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/mhd-faizzan/CampusGuideGPT.git
cd CampusGuideGPT
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure secrets**

Create `.streamlit/secrets.toml`:

```toml
[pinecone]
PINECONE_API_KEY = "your-pinecone-api-key"
PINECONE_INDEX   = "your-index-name"
PINECONE_HOST    = "your-pinecone-host-url"

[groq]
GROQ_API_KEY = "your-groq-api-key"
```

**4. Run**

```bash
streamlit run app.py
```

---

## Limitations

This project was built as academic coursework. The knowledge base contains a limited, curated set of Q&A pairs manually fed into Pinecone in RAG format — it does not cover every aspect of Hochschule Harz or German university processes. Responses are only as good as the data that was indexed. For topics outside the knowledge base, the assistant falls back to general LLM knowledge, which may not always be accurate or up to date. Users should verify important information through official university channels.

---

## License

MIT

---

