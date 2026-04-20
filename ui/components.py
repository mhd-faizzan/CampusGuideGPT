import streamlit as st
import time

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:4px 0 20px; border-bottom:1px solid #333; margin-bottom:20px;">
            <div style="font-size:15px; font-weight:600; color:#e0e0e0;">CampusGuideGPT</div>
            <div style="font-size:11px; color:#6e6e6e; margin-top:2px;">Hochschule Harz AI</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("+ New chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # online status
        st.markdown("""
        <div style="font-size:10px; color:#6e6e6e; letter-spacing:0.8px;
                    text-transform:uppercase; margin-bottom:8px;">Status</div>
        <div style="display:flex; align-items:center; gap:6px; margin-bottom:24px;">
            <div style="width:6px;height:6px;border-radius:50%;background:#4ade80;"></div>
            <span style="font-size:12px;color:#6e6e6e;">Online</span>
        </div>
        """, unsafe_allow_html=True)

        # conversation history
        messages = st.session_state.get("messages", [])
        user_msgs = [m for m in messages if m["role"] == "user"]
        if user_msgs:
            st.markdown("""
            <div style="font-size:10px; color:#6e6e6e; letter-spacing:0.8px;
                        text-transform:uppercase; margin-bottom:8px;">History</div>
            """, unsafe_allow_html=True)
            for m in reversed(user_msgs[-8:]):
                t = m["content"][:44] + "..." if len(m["content"]) > 44 else m["content"]
                st.markdown(f"""
                <div style="padding:7px 10px; border-radius:8px; margin-bottom:2px;
                            cursor:pointer; transition:background 0.15s;"
                     onmouseover="this.style.background='#2a2a2a'"
                     onmouseout="this.style.background='transparent'">
                    <div style="font-size:13px;color:#6e6e6e;white-space:nowrap;
                                overflow:hidden;text-overflow:ellipsis;">{t}</div>
                </div>
                """, unsafe_allow_html=True)

        # footer
        st.markdown("""
        <div style="position:absolute;bottom:16px;left:16px;right:16px;
                    font-size:10px;color:#3a3a3a;border-top:1px solid #2a2a2a;padding-top:10px;">
            © 2024 CampusGuideGPT · Hochschule Harz
        </div>
        """, unsafe_allow_html=True)


def stream_response(text: str):
    """Stream text word by word with typing effect."""
    placeholder = st.empty()
    displayed = ""
    words = text.split(" ")
    for i, word in enumerate(words):
        displayed += word + " "
        placeholder.markdown(
            displayed + '<span class="typing-cursor"></span>',
            unsafe_allow_html=True
        )
        time.sleep(0.03)
    # final render without cursor
    placeholder.markdown(text)
    return text
