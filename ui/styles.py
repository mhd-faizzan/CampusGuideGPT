def load_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    * { font-family: 'Inter', system-ui, sans-serif; box-sizing: border-box; }
    #MainMenu, footer, header { visibility: hidden; }

    /* single dark grey tone throughout */
    :root {
        --bg:       #1e1e1e;
        --surface:  #2a2a2a;
        --border:   #333333;
        --text:     #e0e0e0;
        --muted:    #6e6e6e;
        --accent:   #e0e0e0;
    }

    .stApp { background: var(--bg) !important; }

    /* sidebar */
    [data-testid="stSidebar"] {
        background: #171717 !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] > div { padding-top: 16px; }

    /* all buttons same style */
    .stButton > button {
        background: transparent !important;
        color: var(--muted) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        box-shadow: none !important;
        transition: all 0.15s !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: var(--surface) !important;
        color: var(--text) !important;
        border-color: #4a4a4a !important;
    }

    /* center the main block */
    .main .block-container {
        max-width: 720px !important;
        padding-top: 0 !important;
        padding-bottom: 2rem !important;
    }

    /* chat messages — no background, no border */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 12px 0 !important;
        gap: 14px !important;
    }

    /* message text */
    [data-testid="stChatMessage"] p {
        color: var(--text) !important;
        font-size: 15px !important;
        line-height: 1.8 !important;
        margin: 0 !important;
    }

    /* user bubble */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        flex-direction: row-reverse !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
        background: var(--surface) !important;
        border-radius: 18px 18px 4px 18px !important;
        padding: 12px 16px !important;
        max-width: 80% !important;
    }

    /* avatar icons */
    [data-testid="chatAvatarIcon-user"],
    [data-testid="chatAvatarIcon-assistant"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--muted) !important;
        font-size: 12px !important;
    }

    /* chat input */
    [data-testid="stChatInput"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 4px 4px 4px 16px !important;
    }
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: var(--text) !important;
        font-size: 15px !important;
        border: none !important;
        outline: none !important;
    }
    [data-testid="stChatInput"] textarea::placeholder { color: var(--muted) !important; }
    [data-testid="stChatInput"] button {
        background: var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        margin: 4px !important;
    }
    [data-testid="stChatInput"] button:hover {
        background: #4a4a4a !important;
    }

    /* expander */
    .streamlit-expanderHeader {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--muted) !important;
        font-size: 12px !important;
    }
    .streamlit-expanderContent {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
    }

    /* spinner */
    .stSpinner > div { border-top-color: var(--muted) !important; }

    /* alerts */
    .stAlert {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--muted) !important;
    }

    /* source card */
    .source-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }
    .source-badge {
        font-size: 11px;
        background: var(--border);
        color: var(--muted);
        padding: 2px 8px;
        border-radius: 10px;
    }

    /* typing animation */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0; }
    }
    .typing-cursor {
        display: inline-block;
        width: 2px;
        height: 15px;
        background: var(--muted);
        margin-left: 2px;
        vertical-align: middle;
        animation: blink 0.8s infinite;
    }

    /* divider */
    hr {
        border: none !important;
        border-top: 1px solid var(--border) !important;
        margin: 12px 0 !important;
    }

    /* scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
    </style>
    """
