def load_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    * { font-family: 'Inter', system-ui, sans-serif; box-sizing: border-box; }
    #MainMenu, footer, header { visibility: hidden; }

    .stApp { background: #212121 !important; }

    [data-testid="stSidebar"] {
        background: #171717 !important;
        border-right: 1px solid #2a2a2a !important;
    }
    [data-testid="stSidebar"] > div { padding-top: 16px; }

    .stButton > button {
        background: transparent !important;
        color: #8a8a8a !important;
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

    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 8px 0 !important;
    }

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
        background: #3a3a3a !important;
        border-radius: 8px !important;
        color: #8a8a8a !important;
    }
    [data-testid="stChatInput"] button:hover { background: #4a4a4a !important; }

    [data-testid="stChatMessage"] p {
        color: #ececec !important;
        font-size: 15px !important;
        line-height: 1.75 !important;
    }

    /* vertically center the whole page content */
    .main .block-container {
        min-height: 80vh !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    .stSpinner > div { border-top-color: #8a8a8a !important; }

    .streamlit-expanderHeader {
        background: #2a2a2a !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 10px !important;
        color: #8a8a8a !important;
        font-size: 12px !important;
    }

    .stAlert {
        background: #2f2f2f !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 12px !important;
        color: #8a8a8a !important;
    }

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

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #3a3a3a; border-radius: 4px; }
    </style>
    """
