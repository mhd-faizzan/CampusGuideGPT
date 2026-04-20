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
from ui.components import render_sidebar, stream_response

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

# empty state — centered hero
if not st.session_state.messages:
    st.markdown("""
    <div style="min-height:60vh; display:flex; flex-direction:column;
                align-items:center; justify-content:center; text-align:center;
                padding:40px 20px;">
        <div style="font-size:11px; font-weight:600; color:#6e6e6e;
                    letter-spacing:1.6px; text-transform:uppercase; margin-bottom:12px;">
            Hochschule Harz
        </div>
        <div style="font-size:28px; font-weight:600; color:#e0e0e0;
                    letter-spacing:-0.5px; margin-bottom:14px;">
            CampusGuideGPT
        </div>
        <div style="font-size:15px; color:#6e6e6e; max-width:420px; line-height:1.6;">
            Ask me anything about campus life, admissions, or programs.
        </div>
    </div>
    """, unsafe_allow_html=True)

# render existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("Sources", expanded=False):
                for i, src in enumerate(msg["sources"], 1):
                    pct = int(src["score"] * 100)
                    preview = src["answer"][:160] + "..." if len(src["answer"]) > 160 else src["answer"]
                    st.markdown(f"""
                    <div class="source-card">
                        <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                            <span style="font-size:11px;color:#6e6e6e;font-weight:500;">
                                SOURCE {i:02d}
                            </span>
                            <span class="source-badge">{pct}%</span>
                        </div>
                        <div style="font-size:13px;color:#e0e0e0;margin-bottom:4px;">
                            {src['question']}
                        </div>
                        <div style="font-size:12px;color:#6e6e6e;">{preview}</div>
                    </div>
                    """, unsafe_allow_html=True)

# copyright
st.markdown("""
<div style="text-align:center; padding:16px 0 4px;
            color:#3a3a3a; font-size:11px;">
    © 2024 CampusGuideGPT · Hochschule Harz · All rights reserved
</div>
""", unsafe_allow_html=True)

# chat input
if query := st.chat_input("Ask anything about Hochschule Harz..."):
    # user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # assistant response
    with st.chat_message("assistant"):
        with st.spinner(""):
            hits   = vectors.search(encode(query))
            answer = llm.complete(build_prompt(query, hits))

        if answer:
            # typing animation
            stream_response(answer)

            if hits:
                with st.expander("Sources", expanded=False):
                    for i, src in enumerate(hits, 1):
                        pct = int(src["score"] * 100)
                        preview = src["answer"][:160] + "..." if len(src["answer"]) > 160 else src["answer"]
                        st.markdown(f"""
                        <div class="source-card">
                            <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                                <span style="font-size:11px;color:#6e6e6e;font-weight:500;">
                                    SOURCE {i:02d}
                                </span>
                                <span class="source-badge">{pct}%</span>
                            </div>
                            <div style="font-size:13px;color:#e0e0e0;margin-bottom:4px;">
                                {src['question']}
                            </div>
                            <div style="font-size:12px;color:#6e6e6e;">{preview}</div>
                        </div>
                        """, unsafe_allow_html=True)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": hits,
            })
        else:
            st.error("Could not get a response. Please check your API keys.")
