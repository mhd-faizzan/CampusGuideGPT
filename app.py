import streamlit as st
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import requests

# Load API Keys & Settings from Streamlit Secrets

try:
PINECONE\_API\_KEY = st.secrets\["pinecone"]\["PINECONE\_API\_KEY"]
PINECONE\_INDEX = st.secrets\["pinecone"]\["PINECONE\_INDEX"]
PINECONE\_HOST = st.secrets\["pinecone"]\["PINECONE\_HOST"]
GROQ\_API\_KEY = st.secrets\["groq"]\["GROQ\_API\_KEY"]
except KeyError as e:
st.error(f"Missing API Key in Streamlit secrets: {e}")
st.stop()

# Initialize Pinecone Client and Connect to Index

pc = Pinecone(api\_key=PINECONE\_API\_KEY)
index = pc.Index(PINECONE\_INDEX, host=PINECONE\_HOST)

# Load Embedding Model

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # remove device

# Groq API Setup

GROQ\_URL = "[https://api.groq.com/openai/v1/chat/completions](https://api.groq.com/openai/v1/chat/completions)"
HEADERS = {
"Authorization": f"Bearer {GROQ\_API\_KEY}",
"Content-Type": "application/json"
}

# Initialize session state for history

if "history" not in st.session\_state:
st.session\_state\["history"] = \[]  # Stores (query, response) tuples

# Function to Get Response from Groq API

def get\_groq\_response(prompt):
data = {
"model": "llama-3.3-70b-versatile",
"messages": \[{"role": "user", "content": prompt}],
"max\_tokens": 1024,
"temperature": 0.7,
"top\_p": 0.9,
"stop": \["According to", "Based on", "As per the information"],
}
try:
response = requests.post(GROQ\_URL, headers=HEADERS, json=data)
response.raise\_for\_status()
result = response.json()

```
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
```

# Streamlit UI Styling

st.set\_page\_config(page\_title="CampusGuideGPT", page\_icon="🎓", layout="wide")

# Custom CSS for styling

st.markdown(""" <style>
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
.search-button\:hover {
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
} </style>
""", unsafe\_allow\_html=True)

# Streamlit UI Content

st.markdown('<h1 class="title">CampusGuideGPT</h1>', unsafe\_allow\_html=True)
st.markdown('<p class="sub-title">Ask anything about Hochschule Harz and more universities data coming soon!</p>', unsafe\_allow\_html=True)

# Query System

query = st.text\_input("Enter your question:", placeholder="E.g., How do I apply for a Master's program in Germany?", key="query\_input")

# Enable search on Enter key

if query and st.session\_state.get("query\_input"):
st.session\_state\["search\_triggered"] = True

# Search button

if st.button("Search", key="search\_button", help="Click to get an answer!") or st.session\_state.get("search\_triggered"):
if query:
with st.spinner("Processing your query..."):
query\_embedding = model.encode(query, device='cpu').tolist()

```
        try:
            results = index.query(
                namespace="ns1",
                vector=query_embedding,
                top_k=3,
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
                    # Store query-response pair in session state
                    st.session_state["history"].append((query, response))
                else:
                    st.markdown('<p class="warning">Could not retrieve a specific answer from Groq API. Try asking a different question.</p>', unsafe_allow_html=True)

            else:
                st.markdown('<p class="warning">No matching results found in Pinecone. Falling back to LLM\'s general knowledge...</p>', unsafe_allow_html=True)
                response = get_groq_response(query)
                if response:
                    st.markdown(f'<div class="answer-box"><h3>Answer:</h3><p>{response}</p></div>', unsafe_allow_html=True)
                    # Store query-response pair in session state
                    st.session_state["history"].append((query, response))
                else:
                    st.markdown('<p class="warning">Sorry, we couldn\'t find an answer. Please try again later.</p>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred while querying Pinecone: {e}")
else:
    st.warning("Please enter a question to search.")
