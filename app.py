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

        # Extract the raw response without unnecessary phrases
        llm_response = result['choices'][0]['message']['content']

        # Remove common AI disclaimers
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

# Custom CSS for Enhanced UI
st.markdown("""
    <style>
    /* Main Title Styling */
    .title {
        font-size: 48px;
        color: #2E7D32;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-title {
        font-size: 18px;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
        font-style: italic;
    }
    
    /* Answer Box Styling */
    .answer-box {
        border-left: 5px solid #4CAF50;
        border-radius: 8px;
        padding: 20px;
        background: linear-gradient(135deg, #1e3a1e 0%, #2d5a2d 100%);
        color: white;
        margin-top: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    .answer-box h3 {
        color: #81C784;
        margin-top: 0;
        font-size: 24px;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    
    .answer-box p {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Context Box Styling */
    .context-box {
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 15px;
        margin-top: 20px;
        border-left: 4px solid #2196F3;
    }
    
    .context-box h4 {
        color: #1976D2;
        margin-top: 0;
    }
    
    /* Warning/Info Messages */
    .warning {
        color: #ff6f00;
        font-weight: bold;
        padding: 15px;
        background-color: #fff3e0;
        border-radius: 5px;
        border-left: 4px solid #ff6f00;
    }
    
    /* History Item */
    .history-item {
        background-color: #fafafa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 3px solid #4CAF50;
    }
    
    .history-question {
        font-weight: bold;
        color: #2E7D32;
        margin-bottom: 8px;
    }
    
    .history-answer {
        color: #424242;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Button Styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #45a049 0%, #388E3C 100%);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        font-size: 16px;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76,175,80,0.2);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        margin-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Content
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<h1 class="title">🎓 CampusGuideGPT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Your intelligent assistant for Hochschule Harz and German university information</p>', unsafe_allow_html=True)

# Sidebar for History and Info
with st.sidebar:
    st.markdown("### 📚 About")
    st.info("CampusGuideGPT uses AI to answer your questions about Hochschule Harz and German universities. Ask anything about admissions, programs, campus life, and more!")
    
    st.markdown("### 🔍 Tips for Better Results")
    st.markdown("""
    - Be specific in your questions
    - Ask one question at a time
    - Use clear language
    - Include relevant details
    """)
    
    # Display Search History
    if st.session_state["history"]:
        st.markdown("### 📜 Recent Searches")
        st.markdown(f'<span class="badge">{len(st.session_state["history"])} queries</span>', unsafe_allow_html=True)
        
        with st.expander("View History", expanded=False):
            for i, (q, a) in enumerate(reversed(st.session_state["history"][-5:])):  # Show last 5
                st.markdown(f'<div class="history-item">', unsafe_allow_html=True)
                st.markdown(f'<div class="history-question">Q{len(st.session_state["history"])-i}: {q[:60]}{"..." if len(q) > 60 else ""}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="history-answer">{a[:100]}{"..." if len(a) > 100 else ""}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History"):
            st.session_state["history"] = []
            st.rerun()

# Main Query Interface
query = st.text_input(
    "💬 Ask your question:", 
    placeholder="E.g., How do I apply for a Master's program at Hochschule Harz?", 
    key="query_input",
    label_visibility="collapsed"
)

# Two-column layout for button and status
col_btn, col_status = st.columns([3, 1])

with col_btn:
    search_clicked = st.button("🔍 Search", key="search_button", help="Click to get an answer!", use_container_width=True)

with col_status:
    if st.session_state["history"]:
        st.metric("Queries", len(st.session_state["history"]))

# Process Query
if search_clicked or st.session_state.get("search_triggered"):
    st.session_state["search_triggered"] = False  # Reset trigger
    
    if query:
        with st.spinner("🤔 Processing your query..."):
            try:
                # Generate embedding and ensure it's a flat list
                query_embedding = model.encode(query, convert_to_numpy=True)
                
                # Convert to flat list if it's a numpy array
                if isinstance(query_embedding, np.ndarray):
                    query_embedding = query_embedding.flatten().tolist()
                
                # Debug info (can be removed in production)
                # st.write(f"Debug - Embedding type: {type(query_embedding)}, Length: {len(query_embedding)}")
                
                # Query Pinecone with proper parameters
                results = index.query(
                    vector=query_embedding,  # Changed from query() parameters
                    top_k=3,
                    include_metadata=True,
                    namespace="ns1"
                )

                if results and hasattr(results, 'matches') and results.matches:
                    # Build context from matches
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

                    # Create prompt for Groq
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
                    
                    # Get response from Groq
                    response = get_groq_response(prompt)

                    if response:
                        # Display answer
                        st.markdown(f'<div class="answer-box"><h3>✨ Answer</h3><p>{response}</p></div>', unsafe_allow_html=True)
                        
                        # Store in history
                        st.session_state["history"].append((query, response))
                        
                        # Show sources in expander
                        with st.expander("📖 View Sources", expanded=False):
                            for idx, source in enumerate(sources, 1):
                                st.markdown(f"**Source {idx}** (Relevance: {source['score']:.2%})")
                                st.markdown(f"**Q:** {source['question']}")
                                st.markdown(f"**A:** {source['answer']}")
                                st.divider()
                    else:
                        st.error("Could not retrieve a response from the AI. Please try again.")

                else:
                    # Fallback to general knowledge
                    st.warning("⚠️ No specific information found in the database. Using general knowledge...")
                    
                    fallback_prompt = f"""Answer the following question about German universities or Hochschule Harz based on your general knowledge:

Question: {query}

Provide a helpful answer, but mention that this is general information and the user should verify with official sources."""
                    
                    response = get_groq_response(fallback_prompt)
                    
                    if response:
                        st.markdown(f'<div class="answer-box"><h3>💡 General Information</h3><p>{response}</p></div>', unsafe_allow_html=True)
                        st.info("ℹ️ This answer is based on general knowledge. For official information, please check the Hochschule Harz website.")
                        
                        # Store in history
                        st.session_state["history"].append((query, response))
                    else:
                        st.error("Sorry, we couldn't find an answer. Please try again later.")

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.code(f"Error details: {type(e).__name__}: {str(e)}")
                
                # Debug information
                with st.expander("🔧 Debug Information"):
                    st.write("If this error persists, please check:")
                    st.write("1. Pinecone index configuration")
                    st.write("2. API keys are valid")
                    st.write("3. Network connection")
                    st.write(f"4. Query embedding shape: {len(query_embedding) if 'query_embedding' in locals() else 'Not generated'}")
    else:
        st.warning("⚠️ Please enter a question to search.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 14px;'>
        <p>Powered by Llama 3.3, Pinecone & Sentence Transformers 🚀</p>
        <p>Made with ❤️ for Hochschule Harz students</p>
    </div>
    """, 
    unsafe_allow_html=True
)
