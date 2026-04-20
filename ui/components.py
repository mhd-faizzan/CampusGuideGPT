import streamlit as st

# user bubble — right aligned dark pill
def _user_bubble(text: str):
    st.markdown(f"""
    <div style="display:flex; justify-content:flex-end; margin:16px 0 4px;">
        <div style="background:#2f2f2f; color:#ececec; font-size:15px;
                    line-height:1.6; padding:12px 18px; border-radius:18px 18px 4px 18px;
                    max-width:75%;">
            {text}
        </div>
    </div>
    """, unsafe_allow_html=True)

# assistant bubble — left aligned, no background
def _assistant_bubble(text: str):
    st.markdown(f"""
    <div style="display:flex; align-items:flex-start; gap:12px; margin:16px 0 4px;">
        <div style="width:28px; height:28px; border-radius:50%; background:#2f2f2f;
                    border:1px solid #3a3a3a; flex-shrink:0; display:flex;
                    align-items:center; justify-content:center; font-size:13px;
                    color:#ececec; font-weight:500; margin-top:2px;">C</div>
        <div style="color:#ececec; font-size:15px; line-height:1.75; max-width:80%; padding-top:4px;">
            {text}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_hero():
    st.markdown("""
    <div style="text-align:center; padding:80px 0 40px;">
        <div style="font-size:22px; font-weight:400; color:#ececec; letter-spacing:-0.2px;">
            Ready when you are.
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_answer(response: str, source_count: int = 0, latency_ms: int = 0):
    _assistant_bubble(response)

def render_question(question: str):
    _user_bubble(question)

def render_sources(sources: list[dict]):
    if not sources:
        return
    with st.expander("Sources", expanded=False):
        for i, src in enumerate(sources, 1):
            pct = int(src["score"] * 100)
            preview = src["answer"][:160] + "..." if len(src["answer"]) > 160 else src["answer"]
            st.markdown(f"""
            <div style="background:#2a2a2a; border:1px solid #3a3a3a; border-radius:12px;
                        padding:14px 16px; margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span style="font-size:11px; color:#6a6a6a; font-weight:500;">SOURCE {i:02d}</span>
                    <span style="font-size:11px; background:#3a3a3a; color:#8a8a8a;
                                 padding:2px 8px; border-radius:10px;">{pct}%</span>
                </div>
                <div style="font-size:13px; color:#ececec; margin-bottom:4px;">{src['question']}</div>
                <div style="font-size:12px; color:#6a6a6a;">{preview}</div>
            </div>
            """, unsafe_allow_html=True)

def render_sidebar(history: list[tuple]):
    with st.sidebar:
        st.markdown("""
        <div style="padding:4px 0 20px; border-bottom:1px solid #2a2a2a; margin-bottom:20px;">
            <div style="font-size:15px; font-weight:500; color:#ececec;">CampusGuideGPT</div>
            <div style="font-size:12px; color:#6a6a6a; margin-top:3px;">Hochschule Harz</div>
        </div>
        <div style="font-size:11px; color:#6a6a6a; margin-bottom:6px;
                    letter-spacing:0.8px; text-transform:uppercase;">Status</div>
        <div style="display:flex; align-items:center; gap:6px; margin-bottom:20px;">
            <div style="width:7px; height:7px; border-radius:50%; background:#4ade80;"></div>
            <span style="font-size:12px; color:#8a8a8a;">Online</span>
        </div>
        """, unsafe_allow_html=True)

        if history:
            st.markdown("""
            <div style="font-size:11px; color:#6a6a6a; margin-bottom:8px;
                        letter-spacing:0.8px; text-transform:uppercase;">Recent</div>
            """, unsafe_allow_html=True)
            for q, _ in reversed(history[-6:]):
                truncated = q[:48] + "..." if len(q) > 48 else q
                st.markdown(f"""
                <div style="padding:8px 10px; border-radius:8px; margin-bottom:2px;">
                    <div style="font-size:13px; color:#8a8a8a; white-space:nowrap;
                                overflow:hidden; text-overflow:ellipsis;">{truncated}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Clear history", use_container_width=True):
                st.session_state.history = []
                st.rerun()

def render_footer():
    st.markdown("""
    <div style="text-align:center; padding:24px 0 12px; color:#4a4a4a;
                font-size:11px; border-top:1px solid #2a2a2a; margin-top:32px;">
        CampusGuideGPT · Hochschule Harz · 2024
    </div>
    """, unsafe_allow_html=True)
