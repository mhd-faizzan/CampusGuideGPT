import streamlit as st
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import requests
import numpy as np

# Load API Keys & Settings from Streamlit Secrets
try:
    PINECONE_API_KEY = st.secrets["pinecone"]["PINECONE_API_KEY"]
    PINECONE_INDEX = st.secrets["pinecone"]["PINECONE_INDEX"]
    PINECONE_HOST = st.secrets["pinecone"]["PINECONE_HOST"]
    GROQ_API_KEY = st.secrets["groq"]["GROQ_API_KEY"]
except KeyError as e:
    st.error(f"Missing API Key in Streamlit secrets: {e}")
    st.stop()

# Initialize Pinecone Client and Connect to Index
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)

# Load Embedding Model (cached to avoid reloading)
@st.cache_resource
def load_model():
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

model = load_model()

# Groq API Setup
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Initialize session state
if "history" not in st.session_state:
    st.session_state["history"] = []
if "search_triggered" not in st.session_state:
    st.session_state["search_triggered"] = False

# Function to Get Response from Groq API
def get_groq_response(prompt):
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.7,
        "top_p": 0.9,
        "stop": ["According to", "Based on", "As per the information"],
    }
    try:
        response = requests.post(GROQ_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        result = response.json()

        llm_response = result['choices'][0]['message']['content']

        remove_phrases = [
            "According to the information provided,", 
            "Based on the given data,", 
            "As per the details you provided,",
            "According to the provided information,",
            "Based on the context,",
        ]
        for phrase in remove_phrases:
            llm_response = llm_response.replace(phrase, "").strip()

        return llm_response

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Groq response: {e}")
        return None

# Streamlit UI Configuration
st.set_page_config(
    page_title="CampusGuideGPT", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Dark Theme CSS with Glassmorphism
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Title Section */
    .hero-section {
        text-align: center;
        padding: 60px 20px 40px;
        margin-bottom: 40px;
        position: relative;
    }
    
    .main-title {
        font-size: 72px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 15px;
        letter-spacing: -2px;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .subtitle {
        font-size: 20px;
        color: #a0aec0;
        font-weight: 400;
        margin-bottom: 0;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    .accent-line {
        height: 3px;
        width: 100px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 25px auto;
        border-radius: 10px;
        animation: fadeInUp 0.8s ease-out 0.4s both;
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease-out;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Answer Box with Modern Design */
    .answer-container {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        padding: 30px;
        margin-top: 30px;
        box-shadow: 0 8px 32px 0 rgba(102, 126, 234, 0.2);
        animation: slideInUp 0.5s ease-out;
    }
    
    .answer-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    .answer-icon {
        font-size: 28px;
    }
    
    .answer-title {
        font-size: 24px;
        font-weight: 600;
        color: #e2e8f0;
        margin: 0;
    }
    
    .answer-content {
        color: #cbd5e0;
        font-size: 17px;
        line-height: 1.8;
        font-weight: 400;
    }
    
    /* Source Cards */
    .source-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 3px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .source-card:hover {
        background: rgba(255, 255, 255, 0.06);
        transform: translateX(5px);
    }
    
    .source-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .source-title {
        color: #667eea;
        font-weight: 600;
        font-size: 15px;
    }
    
    .relevance-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .source-question {
        color: #e2e8f0;
        font-weight: 500;
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    .source-answer {
        color: #a0aec0;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* History Items */
    .history-item {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 3px solid #667eea;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .history-item:hover {
        background: rgba(255, 255, 255, 0.06);
        transform: translateX(5px);
    }
    
    .history-question {
        color: #e2e8f0;
        font-weight: 500;
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    .history-answer {
        color: #718096;
        font-size: 13px;
        line-height: 1.5;
    }
    
    .history-time {
        color: #4a5568;
        font-size: 11px;
        margin-top: 5px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1e 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: #e2e8f0;
    }
    
    /* Info/Warning Boxes */
    .stAlert {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        color: #cbd5e0;
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        color: #e2e8f0;
        font-size: 16px;
        padding: 18px 24px;
        transition: all 0.3s ease;
        font-weight: 400;
    }
    
    .stTextInput > div > div > input:focus {
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        outline: none;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #718096;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 18px 40px;
        font-size: 17px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        color: #e2e8f0;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {
        color: #667eea;
        font-size: 28px;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0aec0;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Tag/Badge */
    .tag {
        display: inline-block;
        background: rgba(102, 126, 234, 0.2);
        color: #a0aec0;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(102, 126, 234, 0.5) 50%, transparent 100%);
        margin: 30px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 40px 20px 20px;
        color: #718096;
        font-size: 14px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 60px;
    }
    
    .footer-gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    
    /* Status Indicators */
    .status-online {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #48bb78;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">CampusGuideGPT</h1>
        <div class="accent-line"></div>
        <p class="subtitle">Your intelligent AI assistant for Hochschule Harz & German university insights</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 About CampusGuideGPT")
    st.markdown("""
    <div style='color: #a0aec0; font-size: 14px; line-height: 1.6;'>
    Your AI-powered companion for navigating German university applications, campus life, and academic programs. 
    Powered by advanced language models and semantic search.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 💡 Pro Tips")
    st.markdown("""
    <div style='font-size: 14px;'>
        <span class='tag'>Be specific</span>
        <span class='tag'>One question</span>
        <span class='tag'>Clear context</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stats
    if st.session_state["history"]:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Queries", len(st.session_state["history"]))
        with col2:
            st.metric("Session", "Active", delta="🟢")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # History Section
    if st.session_state["history"]:
        st.markdown("### 📚 Recent History")
        
        with st.expander("View Past Queries", expanded=False):
            for i, (q, a) in enumerate(reversed(st.session_state["history"][-5:])):
                st.markdown(f"""
                <div class="history-item">
                    <div class="history-question">🔹 {q[:70]}{"..." if len(q) > 70 else ""}</div>
                    <div class="history-answer">{a[:120]}{"..." if len(a) > 120 else ""}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🗑️ Clear All History", use_container_width=True):
            st.session_state["history"] = []
            st.rerun()

# Main Content Area
col_left, col_center, col_right = st.columns([0.5, 6, 0.5])

with col_center:
    # Query Input
    query = st.text_input(
        "Ask your question", 
        placeholder="What are the admission requirements for Master's programs?", 
        key="query_input",
        label_visibility="collapsed"
    )
    
    # Search Button
    search_clicked = st.button("🔍 Search Knowledge Base", key="search_button", use_container_width=True)

# Process Query
if search_clicked or st.session_state.get("search_triggered"):
    st.session_state["search_triggered"] = False
    
    if query:
        with col_center:
            with st.spinner("🧠 Analyzing your question..."):
                try:
                    # Generate embedding
                    query_embedding = model.encode(query, convert_to_numpy=True)
                    
                    if isinstance(query_embedding, np.ndarray):
                        query_embedding = query_embedding.flatten().tolist()
                    
                    # Query Pinecone
                    results = index.query(
                        vector=query_embedding,
                        top_k=3,
                        include_metadata=True,
                        namespace="ns1"
                    )

                    if results and hasattr(results, 'matches') and results.matches:
                        # Build context
                        context = ""
                        sources = []
                        
                        for idx, match in enumerate(results.matches, 1):
                            metadata = match.get('metadata', {})
                            question = metadata.get('question', 'N/A')
                            answer = metadata.get('answer', 'N/A')
                            score = match.get('score', 0)
                            
                            context += f"Source {idx}:\nQ: {question}\nA: {answer}\n\n"
                            sources.append({
                                'question': question,
                                'answer': answer,
                                'score': score
                            })

                        # Create prompt
                        prompt = f"""Based on the following context from Hochschule Harz documentation, answer the user's question naturally and conversationally.

Context:
{context}

User Question: {query}

Instructions:
- Provide a clear, direct answer based on the context
- If the context doesn't fully answer the question, say so and provide what information you can
- Be concise but complete
- Use a friendly, helpful tone

Answer:"""
                        
                        response = get_groq_response(prompt)

                        if response:
                            # Display answer with modern styling
                            st.markdown(f"""
                            <div class="answer-container">
                                <div class="answer-header">
                                    <span class="answer-icon">✨</span>
                                    <h3 class="answer-title">Answer</h3>
                                </div>
                                <div class="answer-content">{response}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.session_state["history"].append((query, response))
                            
                            # Sources in expander
                            with st.expander("📖 View Sources & References", expanded=False):
                                for idx, source in enumerate(sources, 1):
                                    relevance_pct = int(source['score'] * 100)
                                    st.markdown(f"""
                                    <div class="source-card">
                                        <div class="source-header">
                                            <span class="source-title">Source {idx}</span>
                                            <span class="relevance-badge">{relevance_pct}% Match</span>
                                        </div>
                                        <div class="source-question"><strong>Q:</strong> {source['question']}</div>
                                        <div class="source-answer"><strong>A:</strong> {source['answer']}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.error("🔴 Could not retrieve a response. Please try again.")

                    else:
                        # Fallback
                        st.warning("⚠️ No specific information found. Using general knowledge...")
                        
                        fallback_prompt = f"""Answer the following question about German universities or Hochschule Harz based on your general knowledge:

Question: {query}

Provide a helpful answer, but mention that this is general information and the user should verify with official sources."""
                        
                        response = get_groq_response(fallback_prompt)
                        
                        if response:
                            st.markdown(f"""
                            <div class="answer-container">
                                <div class="answer-header">
                                    <span class="answer-icon">💡</span>
                                    <h3 class="answer-title">General Information</h3>
                                </div>
                                <div class="answer-content">{response}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.info("ℹ️ This answer is based on general knowledge. Please verify with official sources.")
                            st.session_state["history"].append((query, response))
                        else:
                            st.error("❌ Sorry, couldn't find an answer. Please try again.")

                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    
                    with st.expander("🔧 Technical Details"):
                        st.code(f"{type(e).__name__}: {str(e)}")
                        st.markdown("""
                        **Troubleshooting:**
                        - Check Pinecone index configuration
                        - Verify API keys are valid
                        - Ensure network connectivity
                        """)
    else:
        with col_center:
            st.warning("⚠️ Please enter a question to search.")

# Footer
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 15px;">
        <span class="status-online"></span>
        <span class="footer-gradient-text">System Online</span>
    </div>
    <p>Powered by <strong>Llama 3.3</strong> • <strong>Pinecone Vector DB</strong> • <strong>Sentence Transformers</strong></p>
    <p style="font-size: 12px; margin-top: 10px;">Built with ❤️ for Hochschule Harz • © 2024</p>
</div>
""", unsafe_allow_html=True)
