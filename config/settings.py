import streamlit as st

def load_config():
    return {
        "pinecone_api_key": st.secrets["pinecone"]["PINECONE_API_KEY"],
        "pinecone_index":   st.secrets["pinecone"]["PINECONE_INDEX"],
        "pinecone_host":    st.secrets["pinecone"]["PINECONE_HOST"],
        "groq_api_key":     st.secrets["groq"]["GROQ_API_KEY"],
    }

GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K       = 3
NAMESPACE   = "ns1"
