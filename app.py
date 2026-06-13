
from PyPDF2 import PdfReader
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# -----------------------------
# Load Gemini API
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

if not api_key:
    st.error("Gemini API Key not found in .env file")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-3.5-flash")

# -----------------------------
# App Title
# -----------------------------
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI-Powered Study Buddy")

st.write(
    "Explain topics, summarize notes, generate quizzes, flashcards and study plans using AI."
)

# -----------------------------
# Sidebar Menu
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
# 1. Explain Topic
# ==================================================
if option == "Explain Topic":

    st.header("📖 Explain Topic")

    topic = st.text_input("Enter Topic")

    if st.button("Explain"):

        if topic:

            try:

                with st.spinner("Generating explanation..."):

                    response = model.generate_content(
                        f"""
                        Explain {topic} in simple language.
                        Give examples.
                        Include key points.
                        """
                    )

                st.success("Done!")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.warning("Please enter a topic.")

# ==================================================
# 2. PDF Summarizer
# ==================================================
elif option == "PDF Summarizer":

    st.header("📄 PDF Notes Summarizer")

    uploaded_file = st.file_uploader(
        "Upload PDF Notes",
        type=["pdf"]
    )

    if uploaded_file:

        try:

            pdf_reader = PdfReader(uploaded_file)

            text = ""

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

            st.success("PDF Uploaded Successfully")

            if st.button("Summarize PDF"):

                with st.spinner("Reading PDF..."):

                    response = model.generate_content(
                        f"""
                        Summarize these notes into
                        easy bullet points:

                        {text[:10000]}
                        """
                    )

                st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

# ==================================================
# 3. Quiz Generator
# ==================================================
elif option == "Quiz Generator":

    st.header("❓ Quiz Generator")

    topic = st.text_input("Enter Topic For Quiz")

    if st.button("Generate Quiz"):

        if topic:

            try:

                with st.spinner("Generating Quiz..."):

                    response = model.generate_content(
                        f"""
                        Create 10 multiple choice questions
                        on {topic}.

                        Provide answers at the end.
                        """
                    )

                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.warning("Please enter a topic.")

# ==================================================
# 4. Flashcard Generator
# ==================================================
elif option == "Flashcard Generator":

    st.header("🧠 Flashcard Generator")

    topic = st.text_input("Enter Topic For Flashcards")

    if st.button("Generate Flashcards"):

        if topic:

            try:

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

            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.warning("Please enter a topic.")

# ==================================================
# 5. Study Plan Generator
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

            try:

                with st.spinner("Creating Study Plan..."):

                    response = model.generate_content(
                        f"""
                        Create a detailed {days}-day study plan
                        for {subject}.

                        Divide topics day-wise.

                        Include:
                        - Daily goals
                        - Revision schedule
                        - Practice tests
                        """
                    )

                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.warning("Please enter a subject.")
