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
    try:
        response = requests.post(GROQ_URL, headers=HEADERS, json=data)
        response.raise_for_status()  # Raise error for bad status codes
        result = response.json()
        
        # Extract the raw response without unnecessary phrases
        llm_response = result['choices'][0]['message']['content']

        # Remove common AI disclaimers
        remove_phrases = ["According to the information provided,", "Based on the given data,", "As per the details you provided,"]
        for phrase in remove_phrases:
            llm_response = llm_response.replace(phrase, "").strip()

        return llm_response

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Groq response: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="CampusGuideGPT", page_icon="🎓", layout="wide")

st.title("CampusGuideGPT: AI-powered University Guide")
st.markdown("Ask any question related to studying abroad, especially in Germany, and get AI-powered answers.")

# Query System
query = st.text_input("Enter your question:", placeholder="E.g., How do I apply for a Master's program in Germany?")

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
                    st.success("Here is your answer:")
                    st.write(response)
                else:
                    st.warning("Could not retrieve a specific answer from Groq API. Try asking a different question.")

            else:
                st.warning("No matching results found in Pinecone. Falling back to LLM's general knowledge...")
                response = get_groq_response(query)
                if response:
                    st.success("Here is your answer:")
                    st.write(response)
                else:
                    st.error("Sorry, we couldn't find an answer. Please try again later.")

        except Exception as e:
            st.error(f"An error occurred while querying Pinecone: {e}")

else:
    st.info("Please enter a question above to get started.")
