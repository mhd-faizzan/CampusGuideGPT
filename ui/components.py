import streamlit as st

def render_sidebar():
    with st.sidebar:
        # logo area
        st.markdown("""
        <div style="padding:8px 0 20px;">
            <div style="font-size:16px; font-weight:600; color:#ececec;">
                CampusGuideGPT
            </div>
            <div style="font-size:11px; color:#6a6a6a; margin-top:2px;">
                Hochschule Harz AI
            </div>
        </div>
        """, unsafe_allow_html=True)

        # new chat button
        if st.button("+ New chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # status
        st.markdown("""
        <div style="font-size:11px; color:#6a6a6a; letter-spacing:0.8px;
                    text-transform:uppercase; margin-bottom:8px;">Status</div>
        <div style="display:flex; align-items:center; gap:6px; margin-bottom:20px;">
            <div style="width:7px;height:7px;border-radius:50%;background:#4ade80;"></div>
            <span style="font-size:12px;color:#8a8a8a;">Online</span>
        </div>
        """, unsafe_allow_html=True)

        # recent chats
        messages = st.session_state.get("messages", [])
        user_msgs = [m for m in messages if m["role"] == "user"]
        if user_msgs:
            st.markdown("""
            <div style="font-size:11px; color:#6a6a6a; letter-spacing:0.8px;
                        text-transform:uppercase; margin-bottom:8px;">This session</div>
            """, unsafe_allow_html=True)
            for m in user_msgs[-6:]:
                truncated = m["content"][:46] + "..." if len(m["content"]) > 46 else m["content"]
                st.markdown(f"""
                <div style="padding:8px 10px; border-radius:8px; margin-bottom:2px;
                            cursor:pointer; transition:background 0.15s;"
                     onmouseover="this.style.background='#2a2a2a'"
                     onmouseout="this.style.background='transparent'">
                    <div style="font-size:13px;color:#8a8a8a;white-space:nowrap;
                                overflow:hidden;text-overflow:ellipsis;">{truncated}</div>
                </div>
                """, unsafe_allow_html=True)

        # footer
        st.markdown("""
        <div style="position:absolute; bottom:20px; left:16px; right:16px;
                    font-size:11px; color:#4a4a4a; border-top:1px solid #2a2a2a;
                    padding-top:12px;">
            CampusGuideGPT · 2024
        </div>
        """, unsafe_allow_html=True)
