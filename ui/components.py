import streamlit as st

def render_hero():
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">CampusGuideGPT</h1>
        <div class="accent-line"></div>
        <p class="subtitle">Your intelligent AI assistant for Hochschule Harz & German university insights</p>
    </div>
    """, unsafe_allow_html=True)

def render_answer(response: str):
    st.markdown(f"""
    <div class="answer-container">
        <div class="answer-header">
            <span class="answer-icon">✨</span>
            <h3 class="answer-title">Answer</h3>
        </div>
        <div class="answer-content">{response}</div>
    </div>
    """, unsafe_allow_html=True)

def render_fallback_answer(response: str):
    st.markdown(f"""
    <div class="answer-container">
        <div class="answer-header">
            <span class="answer-icon">💡</span>
            <h3 class="answer-title">General Information</h3>
        </div>
        <div class="answer-content">{response}</div>
    </div>
    """, unsafe_allow_html=True)
    st.info("This answer is based on general knowledge. Please verify with official sources.")

def render_sources(sources: list[dict]):
    if not sources:
        return
    with st.expander("📖 View Sources & References", expanded=False):
        for i, src in enumerate(sources, 1):
            pct = int(src["score"] * 100)
            st.markdown(f"""
            <div class="source-card">
                <div class="source-header">
                    <span class="source-title">Source {i}</span>
                    <span class="relevance-badge">{pct}% Match</span>
                </div>
                <div class="source-question"><strong>Q:</strong> {src['question']}</div>
                <div class="source-answer"><strong>A:</strong> {src['answer']}</div>
            </div>
            """, unsafe_allow_html=True)

def render_sidebar(history: list[tuple]):
    with st.sidebar:
        st.markdown("""
        <div style="padding:4px 0 16px;">
            <div style="font-size:15px;font-weight:600;color:#e2e8f0;">CampusGuideGPT</div>
            <div style="font-size:11px;color:#718096;margin-top:2px;">Hochschule Harz AI</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="color:#a0aec0;font-size:13px;line-height:1.6;margin-bottom:16px;">
            AI-powered assistant for German university applications, campus life, and academic programs.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-bottom:16px;">
            <div style="font-size:12px;font-weight:600;color:#718096;
                        text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px;">
                Pro Tips
            </div>
            <span class="tag">Be specific</span>
            <span class="tag">One question</span>
            <span class="tag">Clear context</span>
        </div>
        """, unsafe_allow_html=True)

        if history:
            c1, c2 = st.columns(2)
            c1.metric("Queries", len(history))
            c2.metric("Session", "Active")
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div style="font-size:12px;font-weight:600;color:#718096;
                        text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px;">
                Recent History
            </div>
            """, unsafe_allow_html=True)

            with st.expander("View Past Queries", expanded=False):
                for q, a in reversed(history[-5:]):
                    st.markdown(f"""
                    <div class="history-item">
                        <div class="history-question">🔹 {q[:70]}{"..." if len(q)>70 else ""}</div>
                        <div class="history-answer">{a[:120]}{"..." if len(a)>120 else ""}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Clear All History", use_container_width=True):
                st.session_state.history = []
                st.rerun()

def render_footer():
    st.markdown("""
    <div class="footer">
        <div style="margin-bottom:12px;">
            <span class="status-online"></span>
            <span class="footer-gradient-text">System Online</span>
        </div>
        <p>Powered by <strong>Llama 3.3</strong> · <strong>Pinecone</strong> · <strong>Sentence Transformers</strong></p>
        <p style="font-size:11px;margin-top:8px;">© 2024 CampusGuideGPT · Hochschule Harz</p>
    </div>
    """, unsafe_allow_html=True)
