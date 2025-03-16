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

# Initialize Session State for Chat Memory
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Function to Get Response from Groq API with Memory
def get_groq_response(prompt, history):
    """Send conversation history and user query to the LLM"""
    messages = [{"role": "system", "content": "You are an AI assistant providing university guidance."}]
    messages += history  # Include past conversations
    messages.append({"role": "user", "content": prompt})

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 1024,
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

# Custom CSS for styling
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        color: #4CAF50;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-title {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .search-button {
        display: block;
        margin: 20px auto;
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
    }
    .warning {
        color: #e65100;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI Content
st.markdown('<h1 class="title">CampusGuideGPT</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Ask anything about Hochschule Harz and more universities data coming soon!</p>', unsafe_allow_html=True)

# User Query Input
query = st.text_input("Enter your question:", placeholder="E.g., How do I apply for a Master's program in Germany?", key="query_input")

# Enable search on Enter key
if query and st.session_state.get("query_input"):
    st.session_state["search_triggered"] = True

# Search button
if st.button("Search", key="search_button", help="Click to get an answer!") or st.session_state.get("search_triggered"):
    if query:
        with st.spinner("Processing your query..."):
            query_embedding = model.encode(query).tolist()

            try:
                # Query Pinecone for relevant context
                results = index.query(namespace="ns1", vector=query_embedding, top_k=3, include_metadata=True)

                if results and "matches" in results:
                    context = ""
                    for match in results["matches"]:
                        context += f"**Question**: {match['metadata']['question']}\n**Answer**: {match['metadata']['answer']}\n\n"

                    prompt = f"Context:\n{context}\n\nUser Question: {query}\nAI Answer:"
                    response = get_groq_response(prompt, st.session_state["chat_history"])

                    if response:
                        # Store conversation history
                        st.session_state["chat_history"].append({"role": "user", "content": query})
                        st.session_state["chat_history"].append({"role": "assistant", "content": response})

                        st.markdown(f'<div class="answer-box"><h3>Answer:</h3><p>{response}</p></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<p class="warning">Could not retrieve a specific answer from Groq API. Try asking a different question.</p>', unsafe_allow_html=True)

                else:
                    # No Pinecone results, fallback to LLM's general knowledge
                    st.markdown('<p class="warning">No matching results found in Pinecone. Falling back to LLM\'s general knowledge...</p>', unsafe_allow_html=True)
                    response = get_groq_response(query, st.session_state["chat_history"])

                    if response:
                        st.session_state["chat_history"].append({"role": "user", "content": query})
                        st.session_state["chat_history"].append({"role": "assistant", "content": response})

                        st.markdown(f'<div class="answer-box"><h3>Answer:</h3><p>{response}</p></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<p class="warning">Sorry, we couldn\'t find an answer. Please try again later.</p>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred while querying Pinecone: {e}")
    else:
        st.warning("Please enter a question to search.")

# Display Chat History
st.markdown("### Chat History")
for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.markdown(f'<div style="color: #2196F3;"><b>You:</b> {chat["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color: #4CAF50;"><b>CampusGuideGPT:</b> {chat["content"]}</div>', unsafe_allow_html=True)
