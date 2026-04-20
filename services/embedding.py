import streamlit as st
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

@st.cache_resource
def _load_model():
    return SentenceTransformer(EMBED_MODEL)

def encode(text: str) -> list[float]:
    vector = _load_model().encode(text, convert_to_numpy=True)
    return vector.flatten().tolist()
