import streamlit as st
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import requests

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

# Load Embedding Model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Groq API Setup
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Function to Get Response from Groq API
def get_groq_response(prompt):
    data = {
        "model": "llama-3.3-70b-versatile",  
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,  
        "temperature": 0.7,  
        "top_p": 0.9,
    }
    try:
        response = requests.post(GROQ_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Groq response: {e}")
        return None

# Streamlit UI Styling
st.set_page_config(page_title="CampusGuideGPT", page_icon="🎓", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    .title {
        font-size: 36px;
        color: #4CAF50;
        font-weight: bold;
        text-align: center;
        overflow: hidden;
        border-right: 3px solid #4CAF50;
        white-space: nowrap;
        width: 100%;
        display: inline-block;
        animation: typing 2s steps(20, end);
    }
    .sub-title {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .search-box {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }
    .search-button {
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        border: none;
        font-size: 18px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .search-button:hover {
        background-color: #45a049;
    }
    .answer-box {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 15px;
        background-color: #2F2F2F;
        color: white;
        margin-top: 20px;
        font-size: 16px;
        line-height: 1.5;
    }
    .warning {
        color: #e65100;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI Content with Typewriter Effect
st.markdown('<h1 class="title">CampusGuideGPT</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Ask anything about Hochschule Harz and more universities data coming soon!</p>', unsafe_allow_html=True)

# Query System with "Enter" key support
def process_query():
    query = st.session_state.query.strip()
    if query:
        with st.spinner("Processing your query..."):
            query_embedding = model.encode(query).tolist()
            try:
                results = index.query(
                    namespace="ns1",
                    vector=query_embedding,
                    top_k=5,
                    include_metadata=True
                )
                if results and "matches" in results:
                    context = ""
                    for match in results["matches"]:
                        context += f"**Question**: {match['metadata']['question']}\n**Answer**: {match['metadata']['answer']}\n\n"
                    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
                    response = get_groq_response(prompt)
                    if response:
                        st.markdown(f'<div class="answer-box"><h3>Answer:</h3><p>{response}</p></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<p class="warning">Could not retrieve a specific answer from Groq API. Try asking a different question.</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="warning">No matching results found in Pinecone. Falling back to LLM\'s general knowledge...</p>', unsafe_allow_html=True)
                    response = get_groq_response(query)
                    if response:
                        st.markdown(f'<div class="answer-box"><h3>Answer:</h3><p>{response}</p></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<p class="warning">Sorry, we couldn\'t find an answer. Please try again later.</p>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred while querying Pinecone: {e}")
    else:
        st.warning("Please enter a question to search.")

# Search Box UI with Single Input Field
txt_input = st.text_input("Ask a question", placeholder="Type here and press Enter", key="query", on_change=process_query)
if st.button("Search", key="search_button", help="Click to get an answer!"):
    process_query()
