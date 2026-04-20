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
from ui.components import render_sidebar

# page config
st.set_page_config(
    page_title="CampusGuideGPT",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.markdown(load_css(), unsafe_allow_html=True)

# init services
cfg     = load_config()
vectors = VectorService(cfg["pinecone_api_key"], cfg["pinecone_index"], cfg["pinecone_host"])
llm     = LLMService(api_key=cfg["groq_api_key"])

# session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# sidebar
render_sidebar()

# show header + subtitle only when no messages
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding:80px 0 16px;">
        <div style="font-size:12px; font-weight:600; color:#6a6a6a;
                    letter-spacing:1.4px; text-transform:uppercase; margin-bottom:10px;">
            Hochschule Harz
        </div>
        <div style="font-size:26px; font-weight:600; color:#ececec; letter-spacing:-0.5px;">
            CampusGuideGPT
        </div>
        <div style="font-size:15px; color:#6a6a6a; margin-top:14px; font-weight:400;">
            Ask me anything about campus life, admissions, or programs.
        </div>
    </div>
    """, unsafe_allow_html=True)

# render conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg and msg["sources"]:
            with st.expander("Sources", expanded=False):
                for i, src in enumerate(msg["sources"], 1):
                    pct = int(src["score"] * 100)
                    preview = src["answer"][:160] + "..." if len(src["answer"]) > 160 else src["answer"]
                    st.markdown(f"""
                    <div class="source-card">
                        <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                            <span style="font-size:11px;color:#6a6a6a;font-weight:500;">SOURCE {i:02d}</span>
                            <span class="source-badge">{pct}%</span>
                        </div>
                        <div style="font-size:13px;color:#ececec;margin-bottom:4px;">{src['question']}</div>
                        <div style="font-size:12px;color:#6a6a6a;">{preview}</div>
                    </div>
                    """, unsafe_allow_html=True)

# copyright
st.markdown("""
<div style="text-align:center; padding:24px 0 8px; color:#4a4a4a; font-size:11px;">
    © 2024 CampusGuideGPT · Hochschule Harz · All rights reserved
</div>
""", unsafe_allow_html=True)

# chat input — always at bottom
if query := st.chat_input("Ask anything about Hochschule Harz..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner(""):
            hits   = vectors.search(encode(query))
            answer = llm.complete(build_prompt(query, hits))

        if answer:
            st.markdown(answer)
            if hits:
                with st.expander("Sources", expanded=False):
                    for i, src in enumerate(hits, 1):
                        pct = int(src["score"] * 100)
                        preview = src["answer"][:160] + "..." if len(src["answer"]) > 160 else src["answer"]
                        st.markdown(f"""
                        <div class="source-card">
                            <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                                <span style="font-size:11px;color:#6a6a6a;font-weight:500;">SOURCE {i:02d}</span>
                                <span class="source-badge">{pct}%</span>
                            </div>
                            <div style="font-size:13px;color:#ececec;margin-bottom:4px;">{src['question']}</div>
                            <div style="font-size:12px;color:#6a6a6a;">{preview}</div>
                        </div>
                        """, unsafe_allow_html=True)
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": hits,
            })
        else:
            st.error("Could not get a response. Please check your API keys.")
