import streamlit as st
from fuzzywuzzy import fuzz, process
from groq import Groq
import time

# Initialize Groq client
client = Groq(api_key=st.secrets["groq"]["GROQ_API_KEY"])

# Custom CSS for improved UI
st.markdown(
    """
    <style>
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .title {
            font-size: 40px;
            color: #4CAF50;
            font-weight: bold;
            text-align: center;
            animation: fadeIn 2s ease-in-out;
        }
        
        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #555;
        }

        .chat-container {
            max-width: 700px;
            margin: auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .chat-bubble {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            max-width: 80%;
            margin-bottom: 10px;
        }
        
        .user-bubble {
            background-color: #ddd;
            color: black;
            text-align: right;
            margin-left: auto;
        }

        .bot-bubble {
            text-align: left;
        }

        .sidebar .sidebar-content {
            background-color: #2d3e50;
            color: white;
            padding: 20px;
        }
        
        .search-button {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }

        .search-button button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 15px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }

        .search-button button:hover {
            background-color: #45a049;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("## CampusGuideGPT Navigation")
st.sidebar.write("Use this assistant to get answers about university-related queries.")

st.markdown('<div class="title">CampusGuideGPT 🎓</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your personal guide to university life. Ask me anything!</div>', unsafe_allow_html=True)

# Predefined Questions and Answers
predefined_qa = [
    {"question": "What is the focus of the Technology and Innovation Management (TIM) program?", "answer": "The TIM program equips students with skills to analyze innovation trends and manage technology."},
    {"question": "What are the application deadlines?", "answer": "For foreign degrees: June 15 (Winter), Dec 15 (Summer). For German degrees: July 15 (Winter), Jan 15 (Summer)."},
    {"question": "Are there tuition fees for the program?", "answer": "No tuition fees, but a semester contribution of 118 EUR applies."},
]

# Function to find the best match for a question
def get_predefined_answer(query):
    threshold = 70
    best_match = process.extractOne(query, [qa["question"] for qa in predefined_qa], scorer=fuzz.partial_ratio)
    if best_match and best_match[1] >= threshold:
        for qa in predefined_qa:
            if qa["question"] == best_match[0]:
                return qa["answer"]
    return None

# Chat UI
def chat_message(message, is_user=False):
    class_name = "user-bubble" if is_user else "bot-bubble"
    st.markdown(f'<div class="chat-bubble {class_name}">{message}</div>', unsafe_allow_html=True)

# Chat Input
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
query = st.text_input("Type your question here...")

# Search Button
if st.button("Search", key="search-button"):
    if query:
        chat_message(query, is_user=True)
        time.sleep(0.5)
        
        predefined_answer = get_predefined_answer(query)
        if predefined_answer:
            chat_message(predefined_answer)
        else:
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": query}],
                    model="llama3-70b-8192"
                )
                chat_message(response.choices[0].message.content)
            except Exception as e:
                chat_message(f"Error fetching AI response: {e}")

st.markdown("</div>", unsafe_allow_html=True)
