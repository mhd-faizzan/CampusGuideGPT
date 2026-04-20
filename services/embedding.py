import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from config.settings import EMBED_MODEL

@st.cache_resource
def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBED_MODEL)

def encode(text: str) -> list[float]:
    model = load_embedding_model()
    vec = model.encode(text, convert_to_numpy=True)
    return vec.flatten().tolist()
