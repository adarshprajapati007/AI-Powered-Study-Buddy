
from PyPDF2 import PdfReader
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# If local .env key not found, try Streamlit Secrets
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        st.error("Gemini API Key not found")
        st.stop()

genai.configure(api_key=api_key)

# -----------------------------
# Gemini Model
# -----------------------------
model = genai.GenerativeModel("models/gemini-3.5-flash")

# -----------------------------
# Title
# -----------------------------
st.title("📚 AI-Powered Study Buddy")

st.write(
    "Explain topics, summarize PDFs, generate quizzes, flashcards, and study plans using AI."
)

# -----------------------------
# Sidebar
# -----------------------------
option = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Explain Topic",
        "PDF Summarizer",
        "Quiz Generator",
        "Flashcard Generator",
        "Study Plan Generator"
    ]
)

# ==================================================
# Explain Topic
# ==================================================
if option == "Explain Topic":

    st.header("📖 Explain Topic")

    topic = st.text_input("Enter Topic")

    if st.button("Explain"):

        if topic:

            with st.spinner("Generating Explanation..."):

                response = model.generate_content(
                    f"""
                    Explain {topic} in simple language.
                    Give examples.
                    Use bullet points.
                    """
                )

            st.write(response.text)

            st.download_button(
                "Download Result",
                response.text,
                file_name="explanation.txt"
            )

# ==================================================
# PDF Summarizer
# ==================================================
elif option == "PDF Summarizer":

    st.header("📄 PDF Summarizer")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        pdf_reader = PdfReader(uploaded_file)

        text = ""

        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

        if st.button("Summarize PDF"):

            with st.spinner("Reading PDF..."):

                response = model.generate_content(
                    f"""
                    Summarize these notes into simple bullet points:

                    {text[:10000]}
                    """
                )

            st.write(response.text)

            st.download_button(
                "Download Summary",
                response.text,
                file_name="summary.txt"
            )

# ==================================================
# Quiz Generator
# ==================================================
elif option == "Quiz Generator":

    st.header("❓ Quiz Generator")

    topic = st.text_input("Enter Topic")

    if st.button("Generate Quiz"):

        if topic:

            with st.spinner("Generating Quiz..."):

                response = model.generate_content(
                    f"""
                    Create 10 MCQs on {topic}.

                    Provide answers at the end.
                    """
                )

            st.write(response.text)

            st.download_button(
                "Download Quiz",
                response.text,
                file_name="quiz.txt"
            )

# ==================================================
# Flashcard Generator
# ==================================================
elif option == "Flashcard Generator":

    st.header("🧠 Flashcard Generator")

    topic = st.text_input("Enter Topic")

    if st.button("Generate Flashcards"):

        if topic:

            with st.spinner("Generating Flashcards..."):

                response = model.generate_content(
                    f"""
                    Create 10 flashcards on {topic}.

                    Format:
                    Question:
                    Answer:
                    """
                )

            st.write(response.text)

            st.download_button(
                "Download Flashcards",
                response.text,
                file_name="flashcards.txt"
            )

# ==================================================
# Study Plan Generator
# ==================================================
elif option == "Study Plan Generator":

    st.header("📅 Study Plan Generator")

    subject = st.text_input("Enter Subject")

    days = st.number_input(
        "Days Left For Exam",
        min_value=1,
        max_value=100,
        value=15
    )

    if st.button("Generate Study Plan"):

        if subject:

            with st.spinner("Creating Study Plan..."):

                response = model.generate_content(
                    f"""
                    Create a detailed {days}-day study plan for {subject}.

                    Include:
                    - Daily Topics
                    - Revision Days
                    - Practice Tests
                    """
                )

            st.write(response.text)

            st.download_button(
                "Download Study Plan",
                response.text,
                file_name="study_plan.txt"
            )
