import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

from config.settings import load_config
from services.embedding import encode
from services.vector_db import VectorService
from services.llm_service import LLMService
from utils.prompt_builder import build_prompt
from ui.styles import load_css
from ui.components import (
    render_hero,
    render_answer,
    render_sources,
    render_sidebar,
    render_footer,
    render_error,
)

# page config
st.set_page_config(
    page_title="CampusGuideGPT",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.markdown(load_css(), unsafe_allow_html=True)

# init services
cfg = load_config()
vectors = VectorService(cfg["pinecone_api_key"], cfg["pinecone_index"], cfg["pinecone_host"])
llm = LLMService(api_key=cfg["groq_api_key"])

# session state
if "history" not in st.session_state:
    st.session_state.history = []

# render sidebar and hero
render_sidebar(st.session_state.history)
render_hero()

# search input
query = st.text_input(
    label="",
    placeholder="Ask anything about Hochschule Harz...",
    label_visibility="collapsed",
)

# on search
if st.button("Ask", use_container_width=True) and query:
    with st.spinner(""):
        hits   = vectors.search(encode(query))
        answer = llm.complete(build_prompt(query, hits))

    if answer:
        render_answer(answer)
        render_sources(hits)
        st.session_state.history.append((query, answer))
    else:
        render_error("Could not get a response. Please check your API keys.")

elif st.session_state.history:
    # show last answer on rerun
    _, last_a = st.session_state.history[-1]
    render_answer(last_a)

render_footer()
