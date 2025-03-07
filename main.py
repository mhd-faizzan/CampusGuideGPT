import streamlit as st
from fuzzywuzzy import fuzz, process
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets["groq"]["GROQ_API_KEY"])

# Predefined Questions and Answers
predefined_qa = [
    {"question": "What is the focus of the Technology and Innovation Management (TIM) program?", "answer": "The Technology and Innovation Management (TIM) program focuses on equipping students with the skills to analyze innovation trends, identify future business opportunities, and make informed decisions about managing innovation."},
    {"question": "How does the TIM program prepare students for careers in innovation and technology?", "answer": "The program prepares students by teaching them to analyze current innovation trends, systematically implement innovation processes, link automation and digitalization solutions with business processes, plan and advocate for projects, and take on management roles in technology-driven environments."},
    {"question": "What is the teaching language of the TIM program?", "answer": "The program is taught entirely in English, with German recommended for better integration into the local environment."},
    {"question": "Are there any fees for the program?", "answer": "There are no tuition fees for this program. However, students are required to pay a semester contribution of 118 EUR, which includes free regional public transportation and a contribution to the student body."},
    {"question": "What are the admission requirements for the TIM program?", "answer": "To qualify for admission: A first university degree with a GPA of 2.5 or higher on the German scale. A degree with at least 180 ECTS credit points for Regular Track or 210 ECTS credit points for Fast Track. A relevant degree in industrial engineering, business informatics, technical management, or a related engineering subject. A minimum of 10 weeks of professional experience related to the previous degree’s subject area. Proof of English proficiency at a B2 level. If the prior degree was conducted in English, no separate language certificate is required."},
    {"question": "What are the deadlines for applications?", "answer": "For applicants with a foreign academic degree (via uni-assist.de): Winter Semester: June 15th, Summer Semester: December 15th. For applicants with a German academic degree (via hs-harz.de): Winter Semester: July 15th, Summer Semester: January 15th."},
    {"question": "What is the difference between the Regular Track and Fast Track?", "answer": "Regular Track (4 semesters): Open to candidates with a 180 ECTS credit degree. Includes an adjustment semester with foundational courses. Fast Track (3 semesters): Open to candidates with a 210 ECTS credit degree. Does not include the adjustment semester."},
    {"question": "What career opportunities does the TIM program offer?", "answer": "Graduates are prepared to support businesses in implementing innovative technologies, manage digitalization processes, pursue managerial roles, and engage in research or doctoral studies."},
    {"question": "Can students opt for internships or an exchange semester during the TIM program?", "answer": "Yes, students can choose to do an internship or an exchange semester abroad. However, this is optional and is recommended only during the fourth semester."},
    {"question": "What core subjects are taught in the TIM program?", "answer": "Core subjects include Strategic Innovation Management, Operations Research, Agile Requirements Engineering, Digital Business Models, Big Data and Geoinformation, Technology Assessment, and more."},
    {"question": "What types of assessments are used in the TIM program?", "answer": "Students are evaluated through project work reports, presentations, written and oral examinations, term papers, software drafts, Master Thesis, and colloquium."},
    {"question": "What options are available for online study?", "answer": "Online study is available only for first-semester students, allowing flexibility for those unable to attend in person initially."},
    {"question": "How does the TIM program incorporate digitalization and Industry 4.0 concepts?", "answer": "The program emphasizes digital transformation strategies, integration of digital tools in business processes, and emerging trends like Mixed Reality and Smart Buildings."},
    {"question": "What is the purpose of the adjustment semester in the Regular Track?", "answer": "The adjustment semester bridges gaps in prior education for students with 180 ECTS credits. It covers foundational topics like Environment, Health, and Safety, Research Fields in Computer Science, and Engineering Projects."},
    {"question": "Where can students find more details about admission requirements and documents?", "answer": "Detailed information about admission requirements and required documents can be found at https://www.hs-harz.de/en/study/degree-students/international-applicants/master/."},
    {"question": "What is the application deadline for the iTIM (International Technology & Innovation Management) program for the summer semester?", "answer": "For applicants with a foreign academic degree (via uni-assist.de): December 15th. For applicants with a German academic degree (via hs-harz.de): January 15th."},
    {"question": "What is the application deadline for the iTIM (International Technology & Innovation Management) program for the winter semester?", "answer": "For applicants with a foreign academic degree (via uni-assist.de): June 15th. For applicants with a German academic degree (via hs-harz.de): July 15th."}

]

# Function to find the best match for a question
def get_predefined_answer(query):
    threshold = 70  # Adjust threshold as needed
    best_match = process.extractOne(query, [qa["question"] for qa in predefined_qa], scorer=fuzz.partial_ratio)
    if best_match and best_match[1] >= threshold:
        for qa in predefined_qa:
            if qa["question"] == best_match[0]:
                return qa["answer"]
    return None

# Streamlit App UI
st.set_page_config(page_title="CampusGuideGPT", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
        body {
            font-family: 'Helvetica', sans-serif;
            background-color: #f4f4f4;
        }
        .title {
            font-size: 40px;
            color: #4CAF50;
        }
        .header {
            font-size: 30px;
            color: #333;
        }
        .sidebar .sidebar-content {
            background-color: #2d3e50;
            color: white;
        }
        .stTextInput>div>div>input {
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">CampusGuideGPT</div>', unsafe_allow_html=True)
st.write("Your personal guide to studying in Germany! Ask me anything about your campus.")

query = st.text_input("Ask your question:")

if query:
    predefined_answer = get_predefined_answer(query)

    if predefined_answer:
        st.write(predefined_answer)
    else:
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": query}],
                model="llama3-70b-8192"
            )
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.write(f"Error fetching AI response: {e}")
