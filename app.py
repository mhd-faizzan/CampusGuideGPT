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
    render_fallback_answer,
    render_sources,
    render_sidebar,
    render_footer,
)

# page config
st.set_page_config(
    page_title="CampusGuideGPT",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(load_css(), unsafe_allow_html=True)

# init services
cfg     = load_config()
vectors = VectorService(cfg["pinecone_api_key"], cfg["pinecone_index"], cfg["pinecone_host"])
llm     = LLMService(api_key=cfg["groq_api_key"])

# session state
if "history" not in st.session_state:
    st.session_state.history = []

# sidebar
render_sidebar(st.session_state.history)

# main layout — centered column
_, col, _ = st.columns([0.5, 6, 0.5])

with col:
    render_hero()

    # input
    query = st.text_input(
        label="",
        placeholder="What are the admission requirements for Master's programs?",
        label_visibility="collapsed",
        key="query_input",
    )

    search = st.button("🔍 Search Knowledge Base", use_container_width=True)

    if search and query:
        with st.spinner("🧠 Analyzing your question..."):
            try:
                vector = encode(query)
                hits   = vectors.search(vector)

                if hits:
                    prompt = build_prompt(query, hits)
                    answer = llm.complete(prompt)

                    if answer:
                        render_answer(answer)
                        render_sources(hits)
                        st.session_state.history.append((query, answer))
                    else:
                        st.error("Could not retrieve a response. Please try again.")
                else:
                    # fallback to general knowledge
                    fallback_prompt = (
                        f"Answer this question about Hochschule Harz or German universities "
                        f"based on general knowledge:\n\nQuestion: {query}\n\n"
                        f"Mention this is general info and user should verify officially."
                    )
                    answer = llm.complete(fallback_prompt)
                    if answer:
                        render_fallback_answer(answer)
                        st.session_state.history.append((query, answer))
                    else:
                        st.error("Could not find an answer. Please try again.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                with st.expander("Technical Details"):
                    st.code(f"{type(e).__name__}: {str(e)}")

    elif search and not query:
        st.warning("Please enter a question to search.")

    render_footer()
