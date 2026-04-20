def load_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap');

    * { font-family: 'Inter', system-ui, sans-serif; box-sizing: border-box; }
    #MainMenu, footer, header { visibility: hidden; }

    /* page */
    .stApp { background: #212121 !important; }

    /* sidebar */
    [data-testid="stSidebar"] {
        background: #171717 !important;
        border-right: 1px solid #2a2a2a !important;
    }

    /* hide default streamlit input label gap */
    .stTextInput > label { display: none; }

    /* input pill */
    .stTextInput > div > div > input {
        background: #2f2f2f !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 28px !important;
        color: #ececec !important;
        font-size: 15px !important;
        padding: 14px 20px !important;
        transition: border-color 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #565656 !important;
        box-shadow: none !important;
        outline: none !important;
    }
    .stTextInput > div > div > input::placeholder { color: #8a8a8a !important; }

    /* send button */
    .stButton > button {
        background: #ececec !important;
        color: #212121 !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 0 !important;
        box-shadow: none !important;
        transition: background 0.15s !important;
        min-height: unset !important;
    }
    .stButton > button:hover { background: #d0d0d0 !important; }

    /* expander for sources */
    .streamlit-expanderHeader {
        background: #2f2f2f !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 12px !important;
        color: #8a8a8a !important;
        font-size: 13px !important;
    }

    /* spinner */
    .stSpinner > div { border-top-color: #8a8a8a !important; }

    /* alerts */
    .stAlert {
        background: #2f2f2f !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 12px !important;
        color: #8a8a8a !important;
        font-size: 13px !important;
    }

    /* scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #3a3a3a; border-radius: 4px; }
    </style>
    """
