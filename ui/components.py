import streamlit as st

def render_hero():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-eyebrow">Hochschule Harz assistant</div>
        <div class="hero-title">Ask anything about <span>campus life</span></div>
        <div class="hero-sub">
            Powered by semantic search across official university documentation
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_chips():
    """Suggestion chips below the search bar."""
    st.markdown("""
    <div class="chip-row">
        <span class="chip">Admission requirements</span>
        <span class="chip">Tuition fees</span>
        <span class="chip">Student visa</span>
        <span class="chip">Semester dates</span>
        <span class="chip">Housing options</span>
    </div>
    """, unsafe_allow_html=True)

def render_answer(response: str, source_count: int = 0, latency_ms: int = 0):
    meta = f"{source_count} sources · {latency_ms}ms" if source_count else ""
    st.markdown(f"""
    <div class="answer-card">
        <div class="answer-header">
            <div class="answer-orb"><div class="answer-orb-inner"></div></div>
            <div>
                <div class="answer-label">Answer</div>
                <div class="answer-meta">{meta}</div>
            </div>
        </div>
        <div class="answer-body">
            <div class="answer-text">{response}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sources(sources: list[dict]):
    if not sources:
        return
    with st.expander("View sources", expanded=False):
        for i, src in enumerate(sources, 1):
            pct = int(src["score"] * 100)
            st.markdown(f"""
            <div class="source-card">
                <div class="source-top">
                    <span class="source-num">Source {i:02d}</span>
                    <span class="source-score">{pct}%</span>
                </div>
                <div class="source-question">{src['question']}</div>
                <div class="source-answer">{src['answer'][:160]}...</div>
            </div>
            """, unsafe_allow_html=True)

def render_sidebar(history: list[tuple]):
    with st.sidebar:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;
                    margin-bottom:24px;padding-bottom:16px;
                    border-bottom:1px solid #1a1a28">
            <div style="width:32px;height:32px;border-radius:8px;
                        background:#1a1a35;border:1px solid #2a2a4a;
                        display:flex;align-items:center;justify-content:center">
                <div style="width:16px;height:8px;border-radius:8px 8px 0 0;
                             background:#6366f1"></div>
            </div>
            <div>
                <div style="font-size:13px;font-weight:600;color:#e2e8f0">
                    CampusGuide
                </div>
                <div style="font-size:10px;color:#4a5068">Hochschule Harz AI</div>
            </div>
        </div>
        <div style="font-size:10px;font-weight:600;color:#3a3a55;
                    letter-spacing:1.2px;text-transform:uppercase;margin-bottom:8px">
            Status
        </div>
        <span class="badge badge-indigo">Llama 3.3 · 70B</span>&nbsp;
        <span class="badge badge-green">Online</span>
        """, unsafe_allow_html=True)

        if history:
            st.markdown("""
            <div style="font-size:10px;font-weight:600;color:#3a3a55;
                        letter-spacing:1.2px;text-transform:uppercase;
                        margin:20px 0 8px">Recent</div>
            """, unsafe_allow_html=True)
            for q, _ in reversed(history[-5:]):
                st.markdown(f"""
                <div class="history-item">
                    <div class="history-q">{q[:55]}{"..." if len(q)>55 else ""}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button("Clear history", use_container_width=True):
                st.session_state.history = []
                st.rerun()

def render_stats(query_count: int):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Documents", "847")
    c2.metric("Queries today", query_count)
    c3.metric("Avg latency", "94ms")
    c4.metric("Uptime", "99%")

def render_footer():
    st.markdown("""
    <div class="app-footer">
        CampusGuideGPT · Hochschule Harz · 2024<br>
        <span class="footer-pill">all-MiniLM-L6-v2</span>
        <span class="footer-pill">Pinecone ns1</span>
        <span class="footer-pill">Groq API</span>
    </div>
    """, unsafe_allow_html=True)
