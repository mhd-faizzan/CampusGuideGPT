def load_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* ── Base ───────────────────────────── */
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
    #MainMenu, footer, header { visibility: hidden; }

    .stApp {
        background: #0d0d12;
    }

    /* ── Sidebar ────────────────────────── */
    [data-testid="stSidebar"] {
        background: #0a0a0f !important;
        border-right: 1px solid #1a1a28 !important;
    }
    [data-testid="stSidebar"] > div { padding-top: 24px; }

    /* ── Input ──────────────────────────── */
    .stTextInput > div > div > input {
        background: #0f0f1a !important;
        border: 1px solid #1e1e30 !important;
        border-radius: 10px !important;
        color: #9a9ab8 !important;
        font-size: 13px !important;
        padding: 12px 16px !important;
        transition: border-color 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.08) !important;
        outline: none !important;
    }
    .stTextInput > div > div > input::placeholder { color: #3a3a55 !important; }

    /* ── Button ─────────────────────────── */
    .stButton > button {
        background: #6366f1 !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        letter-spacing: 0.3px !important;
        transition: background 0.2s, transform 0.1s !important;
        box-shadow: none !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: #4f52d4 !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ── Expander ───────────────────────── */
    .streamlit-expanderHeader {
        background: #0f0f1a !important;
        border: 1px solid #1e1e30 !important;
        border-radius: 10px !important;
        color: #7a7a9a !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }

    /* ── Metrics ────────────────────────── */
    [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-size: 22px !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #3a3a55 !important;
        font-size: 10px !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }
    [data-testid="metric-container"] {
        background: #0d0d18 !important;
        border: 1px solid #1a1a28 !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
    }

    /* ── Alerts ─────────────────────────── */
    .stAlert {
        background: #0f0f1a !important;
        border: 1px solid #1e1e30 !important;
        border-radius: 10px !important;
        color: #7a7a9a !important;
        font-size: 12px !important;
    }

    /* ── Spinner ────────────────────────── */
    .stSpinner > div { border-top-color: #6366f1 !important; }

    /* ── Scrollbar ──────────────────────── */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #1e1e30; border-radius: 4px; }

    /* ── Custom component classes ───────── */
    .hero-section {
        text-align: center;
        padding: 32px 20px 16px;
        margin-bottom: 8px;
    }
    .hero-eyebrow {
        font-size: 10px;
        font-weight: 600;
        color: #6366f1;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 26px;
        font-weight: 600;
        color: #e2e8f0;
        letter-spacing: -0.4px;
        line-height: 1.2;
    }
    .hero-title span { color: #6366f1; }
    .hero-sub {
        font-size: 13px;
        color: #4a5068;
        margin-top: 8px;
        line-height: 1.6;
    }

    /* Answer card */
    .answer-card {
        background: #0f0f1a;
        border: 1px solid #1e1e30;
        border-radius: 12px;
        overflow: hidden;
        margin-top: 8px;
    }
    .answer-header {
        padding: 14px 18px;
        border-bottom: 1px solid #1a1a28;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .answer-orb {
        width: 28px; height: 28px;
        border-radius: 8px;
        background: #13133a;
        border: 1px solid #2a2a5a;
        display: flex; align-items: center; justify-content: center;
    }
    .answer-orb-inner {
        width: 10px; height: 10px;
        border-radius: 50%; background: #6366f1;
    }
    .answer-label {
        font-size: 13px; font-weight: 600; color: #c8c8e8;
    }
    .answer-meta { font-size: 10px; color: #4a5068; }
    .answer-body { padding: 18px; }
    .answer-text {
        font-size: 13px;
        color: #8a8aaa;
        line-height: 1.75;
    }
    .answer-text strong { color: #c8c8e8; font-weight: 500; }

    /* Source card */
    .source-card {
        background: #0d0d18;
        border: 1px solid #1a1a28;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
        transition: border-color 0.15s;
    }
    .source-card:hover { border-color: #2a2a48; }
    .source-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .source-num { font-size: 10px; font-weight: 600; color: #6366f1; }
    .source-score {
        font-size: 10px;
        padding: 2px 8px;
        border-radius: 10px;
        background: #13133a;
        color: #6366f1;
        border: 1px solid #1e1e4a;
        font-weight: 600;
    }
    .source-question {
        font-size: 11px; color: #7a7a9a; line-height: 1.5;
    }
    .source-answer {
        font-size: 11px; color: #4a5068;
        margin-top: 6px; line-height: 1.5;
    }

    /* History item */
    .history-item {
        padding: 8px 10px;
        border-radius: 8px;
        margin-bottom: 4px;
        cursor: pointer;
        border: 1px solid transparent;
        transition: all 0.15s;
    }
    .history-item:hover {
        background: #13131f;
        border-color: #1e1e35;
    }
    .history-q {
        font-size: 11px; color: #7a7a9a;
        white-space: nowrap; overflow: hidden;
        text-overflow: ellipsis;
    }
    .history-time { font-size: 10px; color: #3a3a55; margin-top: 2px; }

    /* Suggestion chips */
    .chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 4px 0 12px; }
    .chip {
        font-size: 11px;
        padding: 5px 12px;
        border-radius: 20px;
        background: #0f0f1a;
        border: 1px solid #1e1e30;
        color: #5a5a78;
        cursor: pointer;
        transition: border-color 0.15s, color 0.15s;
        display: inline-block;
    }
    .chip:hover { border-color: #6366f1; color: #9a9abb; }

    /* Status badge */
    .badge {
        font-size: 10px;
        padding: 3px 8px;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
    }
    .badge-indigo { background: #0f1a2e; color: #6366f1; border: 1px solid #1e2a4a; }
    .badge-green  { background: #0a1f12; color: #4ade80; border: 1px solid #1a3a20; }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 24px 20px 16px;
        color: #3a3a55;
        font-size: 10px;
        border-top: 1px solid #1a1a28;
        margin-top: 32px;
    }
    .footer-pill {
        display: inline-block;
        font-size: 9px;
        padding: 3px 8px;
        border-radius: 10px;
        background: #0f0f1a;
        color: #3a3a55;
        border: 1px solid #1a1a28;
        margin: 0 3px;
    }
    </style>
    """
