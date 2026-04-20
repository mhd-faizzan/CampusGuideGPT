def load_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap');

    * { font-family: 'Inter', system-ui, sans-serif; box-sizing: border-box; }
    #MainMenu, footer, header { visibility: hidden; }

    /* background */
    .stApp { background: #212121 !important; }

    /* sidebar */
    [data-testid="stSidebar"] {
        background: #171717 !important;
        border-right: 1px solid #2a2a2a !important;
    }

    /* input — pill shaped */
    .stTextInput > div > div > input {
        background: #2f2f2f !important;
        border: 1px solid #2f2f2f !important;
        border-radius: 28px !important;
        color: #ececec !important;
        font-size: 15px !important;
        padding: 14px 20px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4a4a4a !important;
        box-shadow: none !important;
        outline: none !important;
    }
    .stTextInput > div > div > input::placeholder { color: #8a8a8a !important; }

    /* button */
    .stButton > button {
        background: #2f2f2f !important;
        color: #ececec !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 28px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 12px 24px !important;
        width: 100%;
        box-shadow: none !important;
        transition: background 0.15s !important;
    }
    .stButton > button:hover {
        background: #3a3a3a !important;
        border-color: #4a4a4a !important;
    }

    /* expander */
    .streamlit-expanderHeader {
        background: #2f2f2f !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 12px !important;
        color: #8a8a8a !important;
        font-size: 13px !important;
    }

    /* spinner */
    .stSpinner > div { border-top-color: #676767 !important; }

    /* alerts */
    .stAlert {
        background: #2f2f2f !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 12px !important;
        color: #8a8a8a !important;
    }

    /* scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #3a3a3a; border-radius: 4px; }
    </style>
    """
