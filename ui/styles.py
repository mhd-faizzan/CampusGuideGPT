def load_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }

    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    }

    /* sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1e 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* input */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
        border-radius: 15px !important;
        color: #e2e8f0 !important;
        font-size: 16px !important;
        padding: 18px 24px !important;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border: 2px solid #667eea !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.2) !important;
        background: rgba(255,255,255,0.08) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #718096 !important; }

    /* button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 14px 40px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102,126,234,0.6) !important;
    }

    /* expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-weight: 500 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    .streamlit-expanderHeader:hover {
        background: rgba(255,255,255,0.08) !important;
        border-color: rgba(102,126,234,0.3) !important;
    }

    /* alerts */
    .stAlert {
        background: rgba(102,126,234,0.1) !important;
        border: 1px solid rgba(102,126,234,0.3) !important;
        border-radius: 12px !important;
        color: #cbd5e0 !important;
    }

    /* metrics */
    [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #a0aec0 !important;
        font-size: 13px !important;
    }

    /* spinner */
    .stSpinner > div { border-top-color: #667eea !important; }

    /* scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    /* hero */
    .hero-section {
        text-align: center;
        padding: 56px 20px 36px;
        margin-bottom: 32px;
    }
    .main-title {
        font-size: 64px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
        letter-spacing: -2px;
        animation: fadeInUp 0.8s ease-out;
    }
    .subtitle {
        font-size: 18px;
        color: #a0aec0;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    .accent-line {
        height: 3px;
        width: 100px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 20px auto;
        border-radius: 10px;
    }

    /* answer container */
    .answer-container {
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(102,126,234,0.3);
        padding: 28px;
        margin-top: 28px;
        box-shadow: 0 8px 32px rgba(102,126,234,0.2);
        animation: slideInUp 0.5s ease-out;
    }
    .answer-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 18px;
        padding-bottom: 14px;
        border-bottom: 2px solid rgba(102,126,234,0.3);
    }
    .answer-icon  { font-size: 26px; }
    .answer-title { font-size: 22px; font-weight: 600; color: #e2e8f0; margin: 0; }
    .answer-content {
        color: #cbd5e0;
        font-size: 16px;
        line-height: 1.8;
    }

    /* source card */
    .source-card {
        background: rgba(255,255,255,0.03);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 12px;
        border-left: 3px solid #667eea;
        transition: all 0.3s ease;
    }
    .source-card:hover {
        background: rgba(255,255,255,0.06);
        transform: translateX(5px);
    }
    .source-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .source-title   { color: #667eea; font-weight: 600; font-size: 14px; }
    .relevance-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }
    .source-question { color: #e2e8f0; font-weight: 500; font-size: 13px; margin-bottom: 6px; }
    .source-answer   { color: #a0aec0; font-size: 13px; line-height: 1.5; }

    /* history item */
    .history-item {
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 3px solid #667eea;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .history-item:hover {
        background: rgba(255,255,255,0.06);
        transform: translateX(4px);
    }
    .history-question { color: #e2e8f0; font-weight: 500; font-size: 13px; margin-bottom: 5px; }
    .history-answer   { color: #718096; font-size: 12px; line-height: 1.4; }

    /* tag */
    .tag {
        display: inline-block;
        background: rgba(102,126,234,0.2);
        color: #a0aec0;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid rgba(102,126,234,0.3);
    }

    /* status dot */
    .status-online {
        display: inline-block;
        width: 8px; height: 8px;
        background: #48bb78;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }

    /* footer */
    .footer {
        text-align: center;
        padding: 36px 20px 16px;
        color: #718096;
        font-size: 13px;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 56px;
    }
    .footer-gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }

    /* divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(102,126,234,0.5), transparent) !important;
        margin: 28px 0 !important;
    }

    /* animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.5; }
    }
    </style>
    """
