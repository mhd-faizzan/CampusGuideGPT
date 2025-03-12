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
        "model": "llama-3.3-70b-versatile",  # Updated model
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,  # Adjust if needed
        "temperature": 0.7,  # Controls creativity
        "top_p": 0.9,
        "stop": ["According to", "Based on", "As per the information"],  # Prevents robotic phrases
    }
    response = requests.post(GROQ_URL, headers=HEADERS, json=data)
    result = response.json()
    
    # Extract the raw response without unnecessary phrases
    llm_response = result['choices'][0]['message']['content']

    # Remove common AI disclaimers
    remove_phrases = ["According to the information provided,", "Based on the given data,", "As per the details you provided,"]
    for phrase in remove_phrases:
        llm_response = llm_response.replace(phrase, "").strip()

    return llm_response

# Streamlit UI
st.title("CampusGuideGPT (Powered by Pinecone & Groq)")

# Query System
query = st.text_input("Enter your question:")

if query:
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
                context += f"Question: {match['metadata']['question']}\nAnswer: {match['metadata']['answer']}\n\n"

            prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
            response = get_groq_response(prompt)

            if response:
                st.write("### Answer:")
                st.write(response)
        else:
            st.warning("No matching results found in Pinecone. Falling back to LLM's general knowledge...")
            response = get_groq_response(query)
            st.write("### Answer:")
            st.write(response)

    except Exception as e:
        st.error(f"Error querying Pinecone: {e}")
