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

# Streamlit UI Styling
st.set_page_config(page_title="CampusGuideGPT", page_icon="🎓", layout="wide")

# Typewriter Effect for Title (Using JavaScript)
st.markdown("""
    <style>
    .title-container {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #4CAF50;
        margin-top: 20px;
    }
    </style>

    <div class="title-container">
        <span id="typewriter"></span>
    </div>

    <script>
    var text = "CampusGuideGPT";
    var i = 0;
    function typeEffect() {
        if (i < text.length) {
            document.getElementById("typewriter").innerHTML += text.charAt(i);
            i++;
            setTimeout(typeEffect, 150); // Adjust speed of typing
        }
    }
    typeEffect();
    </script>
""", unsafe_allow_html=True)

# Subtitle
st.markdown("<p style='text-align: center; font-size: 20px; color: #555;'>Ask anything about Hochschule Harz and more universities coming soon!</p>", unsafe_allow_html=True)

# Query System
query = st.text_input("Enter your question:", placeholder="E.g., How do I apply for a Master's program in Germany?")

# Search button
if st.button("Search"):
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

                    response = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
                    
                    st.markdown(f'<div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 15px; background-color: #2F2F2F; color: white; margin-top: 20px;"><h3>Answer:</h3><p>{response}</p></div>', unsafe_allow_html=True)

                else:
                    st.warning("No matching results found in Pinecone. Falling back to LLM's general knowledge...")
                    response = query  # Placeholder for actual LLM response
                    st.markdown(f'<div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 15px; background-color: #2F2F2F; color: white; margin-top: 20px;"><h3>Answer:</h3><p>{response}</p></div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred while querying Pinecone: {e}")
    else:
        st.warning("Please enter a question to search.")
