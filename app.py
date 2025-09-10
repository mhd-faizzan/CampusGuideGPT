import streamlit as st
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import requests
import time
from datetime import datetime
import json

# ======================
# PAGE CONFIGURATION
# ======================
st.set_page_config(
    page_title="CampusGuideGPT",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# MODERN CSS STYLING
# ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #2563EB;
        --primary-dark: #1D4ED8;
        --secondary: #10B981;
        --accent: #8B5CF6;
        --bg-primary: #0F172A;
        --bg-secondary: #1E293B;
        --bg-tertiary: #334155;
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted: #94A3B8;
        --border: #475569;
        --success: #22C55E;
        --warning: #F59E0B;
        --error: #EF4444;
        --gradient: linear-gradient(135deg, var(--primary), var(--accent));
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Header Styling */
    .main-header {
        background: var(--gradient);
        padding: 2rem 0;
        border-radius: 0 0 2rem 2rem;
        margin: -1rem -2rem 3rem -2rem;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Search Container */
    .search-container {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 1rem;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.75rem !important;
        color: var(--text-primary) !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        height: 3.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: var(--gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Response Cards */
    .response-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 1rem;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--primary);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .response-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        gap: 0.75rem;
    }
    
    .bot-avatar {
        width: 40px;
        height: 40px;
        background: var(--gradient);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    
    .response-content {
        color: var(--text-primary);
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .query-display {
        background: var(--bg-tertiary);
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 3px solid var(--secondary);
    }
    
    /* History Sidebar */
    .history-item {
        background: var(--bg-tertiary);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border-left: 3px solid transparent;
    }
    
    .history-item:hover {
        background: var(--bg-secondary);
        border-left-color: var(--primary);
        transform: translateX(4px);
    }
    
    .history-query {
        font-weight: 500;
        color: var(--text-primary);
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }
    
    .history-time {
        font-size: 0.75rem;
        color: var(--text-muted);
    }
    
    /* Status Messages */
    .status-processing {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #93C5FD;
        padding: 1rem;
        border-radius: 0.75rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .status-success {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        color: #86EFAC;
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #FCD34D;
    }
    
    .status-error {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #FCA5A5;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: var(--bg-secondary);
    }
    
    .sidebar-content {
        padding: 1rem;
    }
    
    /* Metrics Cards */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Loading Animation */
    .loading-dots {
        display: inline-block;
    }
    
    .loading-dots:after {
        content: '';
        animation: dots 1.5s steps(5, end) infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: ''; }
        40% { content: '.'; }
        60% { content: '..'; }
        80%, 100% { content: '...'; }
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        color: var(--text-muted);
        padding: 2rem 0;
        border-top: 1px solid var(--border);
        margin-top: 3rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# API CONFIGURATION
# ======================
@st.cache_data
def load_config():
    """Load API keys and configuration from Streamlit secrets"""
    try:
        config = {
            "PINECONE_API_KEY": st.secrets["pinecone"]["PINECONE_API_KEY"],
            "PINECONE_INDEX": st.secrets["pinecone"]["PINECONE_INDEX"],
            "PINECONE_HOST": st.secrets["pinecone"]["PINECONE_HOST"],
            "GROQ_API_KEY": st.secrets["groq"]["GROQ_API_KEY"]
        }
        return config
    except KeyError as e:
        st.error(f"🔒 Missing API Key in Streamlit secrets: {e}")
        st.info("Please configure your API keys in the Streamlit secrets management.")
        st.stop()

config = load_config()

# ======================
# INITIALIZE SERVICES
# ======================
@st.cache_resource
def initialize_services():
    """Initialize Pinecone, embedding model, and other services"""
    # Initialize Pinecone
    pc = Pinecone(api_key=config["PINECONE_API_KEY"])
    index = pc.Index(config["PINECONE_INDEX"], host=config["PINECONE_HOST"])
    
    # Load embedding model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    return pc, index, model

pc, index, model = initialize_services()

# Groq API Setup
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {config['GROQ_API_KEY']}",
    "Content-Type": "application/json"
}

# ======================
# SESSION STATE INITIALIZATION
# ======================
if "history" not in st.session_state:
    st.session_state.history = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "current_query" not in st.session_state:
    st.session_state.current_query = ""
if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = 0

# ======================
# CORE FUNCTIONS
# ======================
def get_groq_response(prompt):
    """Enhanced Groq API response with better error handling"""
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.7,
        "top_p": 0.9,
        "stop": ["According to", "Based on", "As per the information"],
    }
    
    try:
        start_time = time.time()
        response = requests.post(GROQ_URL, headers=HEADERS, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Calculate response time
        response_time = time.time() - start_time
        st.session_state.last_response_time = response_time
        
        # Extract and clean response
        llm_response = result['choices'][0]['message']['content']
        
        # Remove common AI disclaimers
        remove_phrases = [
            "According to the information provided,", 
            "Based on the given data,", 
            "As per the details you provided,"
        ]
        for phrase in remove_phrases:
            llm_response = llm_response.replace(phrase, "").strip()
        
        return llm_response
        
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timeout. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"🌐 Network error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"🚫 Unexpected error: {str(e)}")
        return None

def search_knowledge_base(query, top_k=3):
    """Search the knowledge base with enhanced error handling"""
    try:
        query_embedding = model.encode(query, device='cpu').tolist()
        
        results = index.query(
            namespace="ns1",
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        if results and "matches" in results and results["matches"]:
            context = ""
            for match in results["matches"]:
                if match.get('metadata'):
                    context += f"**Q**: {match['metadata'].get('question', 'N/A')}\n"
                    context += f"**A**: {match['metadata'].get('answer', 'N/A')}\n\n"
            return context, len(results["matches"])
        
        return None, 0
        
    except Exception as e:
        st.error(f"🔍 Knowledge base search error: {str(e)}")
        return None, 0

def add_to_history(query, response):
    """Add query-response pair to history with timestamp"""
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.history.insert(0, {
        "query": query,
        "response": response,
        "timestamp": timestamp,
        "id": len(st.session_state.history)
    })
    st.session_state.query_count += 1

# ======================
# UI COMPONENTS
# ======================
def render_header():
    """Render the main header"""
    st.markdown("""
        <div class="main-header">
            <h1 class="app-title">🎓 CampusGuideGPT</h1>
            <p class="app-subtitle">
                Your intelligent companion for Hochschule Harz information and university guidance
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_metrics():
    """Render metrics cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{st.session_state.query_count}</div>
                <div class="metric-label">Queries Processed</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        response_time = f"{st.session_state.last_response_time:.2f}s" if st.session_state.last_response_time > 0 else "N/A"
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{response_time}</div>
                <div class="metric-label">Last Response Time</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(st.session_state.history)}</div>
                <div class="metric-label">Session History</div>
            </div>
        """, unsafe_allow_html=True)

def render_response_card(query, response, show_query=True):
    """Render a styled response card"""
    card_html = '<div class="response-card">'
    
    if show_query:
        card_html += f"""
            <div class="query-display">
                <strong>🤔 Your Question:</strong><br>
                {query}
            </div>
        """
    
    card_html += f"""
        <div class="response-header">
            <div class="bot-avatar">🤖</div>
            <div>
                <strong>CampusGuide AI</strong>
                <div style="font-size: 0.8rem; color: var(--text-muted);">
                    {datetime.now().strftime("%H:%M:%S")}
                </div>
            </div>
        </div>
        <div class="response-content">
            {response}
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with history and controls"""
    with st.sidebar:
        st.markdown("### 📊 Session Overview")
        
        # Quick stats
        if st.session_state.query_count > 0:
            st.metric("Queries Today", st.session_state.query_count)
            if st.session_state.last_response_time > 0:
                st.metric("Avg Response", f"{st.session_state.last_response_time:.1f}s")
        
        st.markdown("---")
        
        # Search history
        if st.session_state.history:
            st.markdown("### 🕒 Recent Queries")
            
            for idx, item in enumerate(st.session_state.history[:5]):  # Show last 5
                query_preview = item["query"][:50] + "..." if len(item["query"]) > 50 else item["query"]
                
                history_html = f"""
                    <div class="history-item" onclick="document.getElementById('query_input').value='{item['query'].replace("'", "\\'")}'; document.getElementById('query_input').dispatchEvent(new Event('input'));">
                        <div class="history-query">{query_preview}</div>
                        <div class="history-time">{item['timestamp']}</div>
                    </div>
                """
                st.markdown(history_html, unsafe_allow_html=True)
            
            if st.button("🗑️ Clear History", type="secondary"):
                st.session_state.history = []
                st.session_state.query_count = 0
                st.rerun()
        else:
            st.markdown("*No queries yet. Start asking questions!*")
        
        st.markdown("---")
        
        # Help section
        st.markdown("### 💡 Tips")
        st.markdown("""
        - **Be specific** in your questions
        - Ask about **admissions, programs, campus life**
        - Try **"How do I apply for..."** queries
        - Use **clear, simple language**
        """)
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About CampusGuideGPT"):
            st.markdown("""
            **CampusGuideGPT** is an AI-powered assistant specifically designed 
            to help students and prospective students with information about 
            Hochschule Harz and general university guidance.
            
            **Features:**
            - 🎯 Specialized knowledge base
            - ⚡ Fast AI responses
            - 📚 Academic information
            - 🔍 Intelligent search
            """)

# ======================
# MAIN APPLICATION
# ======================
def main():
    """Main application logic"""
    render_header()
    render_metrics()
    render_sidebar()
    
    # Main search interface
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Search input with enhanced styling
    st.markdown("### 🔍 Ask Your Question")
    st.markdown("*Ask anything about Hochschule Harz, admissions, programs, student life, and more...*")
    
    # Create columns for better layout
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "",
            placeholder="E.g., How do I apply for a Master's program in Computer Science?",
            key="query_input",
            label_visibility="collapsed"
        )
    
    with col2:
        search_clicked = st.button("🚀 Search", type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process search query
    if (search_clicked or (query and query != st.session_state.current_query)) and query.strip():
        st.session_state.current_query = query
        
        with st.spinner("🔄 Processing your query..."):
            # Search progress indicator
            progress_placeholder = st.empty()
            progress_placeholder.markdown(
                '<div class="status-processing">🔍 Searching knowledge base<span class="loading-dots"></span></div>',
                unsafe_allow_html=True
            )
            
            # Search knowledge base
            context, matches_found = search_knowledge_base(query)
            
            if context:
                progress_placeholder.markdown(
                    '<div class="status-processing">🧠 Generating intelligent response<span class="loading-dots"></span></div>',
                    unsafe_allow_html=True
                )
                
                # Create enhanced prompt
                prompt = f"""Context from Hochschule Harz knowledge base:\n{context}\n\nStudent Question: {query}\n\nProvide a helpful, accurate answer based on the context above. If the context doesn't fully answer the question, supplement with general knowledge about German universities and higher education."""
                
                response = get_groq_response(prompt)
                progress_placeholder.empty()
                
                if response:
                    st.markdown(
                        f'<div class="status-success">✅ Found {matches_found} relevant matches in knowledge base</div>',
                        unsafe_allow_html=True
                    )
                    render_response_card(query, response)
                    add_to_history(query, response)
                else:
                    st.markdown(
                        '<div class="status-error">❌ Failed to generate response. Please try again.</div>',
                        unsafe_allow_html=True
                    )
            
            else:
                # Fallback to general knowledge
                progress_placeholder.markdown(
                    '<div class="status-warning">⚠️ No specific matches found. Using general knowledge<span class="loading-dots"></span></div>',
                    unsafe_allow_html=True
                )
                
                response = get_groq_response(query)
                progress_placeholder.empty()
                
                if response:
                    st.markdown(
                        '<div class="status-warning">💡 Response based on general knowledge</div>',
                        unsafe_allow_html=True
                    )
                    render_response_card(query, response)
                    add_to_history(query, response)
                else:
                    st.markdown(
                        '<div class="status-error">❌ Sorry, we couldn\'t generate a response. Please try again later.</div>',
                        unsafe_allow_html=True
                    )
    
    elif search_clicked and not query.strip():
        st.warning("⚠️ Please enter a question to search.")
    
    # Display conversation history
    if st.session_state.history:
        st.markdown("### 💬 Conversation History")
        
        # Show recent conversations (limit to 3 for performance)
        for item in st.session_state.history[:3]:
            with st.expander(f"🕒 {item['timestamp']} - {item['query'][:60]}{'...' if len(item['query']) > 60 else ''}", expanded=False):
                render_response_card(item['query'], item['response'], show_query=False)
    
    # Footer
    st.markdown("""
        <div class="app-footer">
            <p>🎓 CampusGuideGPT • Powered by Advanced AI • Built for Students</p>
            <p style="font-size: 0.8rem; margin-top: 0.5rem;">
                Made with ❤️ using Streamlit, Groq AI, and Pinecone Vector Database
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
