def load_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    * { font-family: 'Inter', system-ui, sans-serif; box-sizing: border-box; }
    #MainMenu, footer, header { visibility: hidden; }

    /* page background */
    .stApp { background: #212121 !important; }

    /* sidebar */
    [data-testid="stSidebar"] {
        background: #171717 !important;
        border-right: 1px solid #2a2a2a !important;
    }
    [data-testid="stSidebar"] > div { padding-top: 16px; }

    /* new chat button */
    .stButton > button {
        background: transparent !important;
        color: #ececec !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        box-shadow: none !important;
        transition: background 0.15s !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: #2a2a2a !important;
        border-color: #4a4a4a !important;
    }

    /* chat messages */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 8px 0 !important;
    }

    /* user message bubble */
    [data-testid="stChatMessage"][data-testid*="user"] {
        flex-direction: row-reverse !important;
    }

    /* chat input */
    [data-testid="stChatInput"] {
        background: #2f2f2f !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 16px !important;
    }
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #ececec !important;
        font-size: 15px !important;
        border: none !important;
    }
    [data-testid="stChatInput"] textarea::placeholder { color: #8a8a8a !important; }
    [data-testid="stChatInput"] button {
        background: #ececec !important;
        border-radius: 8px !important;
        color: #212121 !important;
    }
    [data-testid="stChatInput"] button:hover { background: #d0d0d0 !important; }

    /* assistant message text */
    [data-testid="stChatMessage"] p {
        color: #ececec !important;
        font-size: 15px !important;
        line-height: 1.75 !important;
    }

    /* spinner */
    .stSpinner > div { border-top-color: #8a8a8a !important; }

    /* expander */
    .streamlit-expanderHeader {
        background: #2a2a2a !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 10px !important;
        color: #8a8a8a !important;
        font-size: 12px !important;
    }

    /* alerts */
    .stAlert {
        background: #2f2f2f !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 12px !important;
        color: #8a8a8a !important;
    }

    /* source card */
    .source-card {
        background: #2a2a2a;
        border: 1px solid #3a3a3a;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }
    .source-badge {
        font-size: 11px;
        background: #3a3a3a;
        color: #8a8a8a;
        padding: 2px 8px;
        border-radius: 10px;
    }

    /* suggestion chips */
    .suggestion-chip {
        display: inline-block;
        background: #2f2f2f;
        border: 1px solid #3a3a3a;
        color: #8a8a8a;
        font-size: 13px;
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
    }

    /* scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #3a3a3a; border-radius: 4px; }
    </style>
    """
