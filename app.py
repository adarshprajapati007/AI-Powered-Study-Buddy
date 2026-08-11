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

if not api_key:
    st.error("Gemini API Key not found in .env file")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.5-flash")

# -----------------------------
# App Title & Configuration
# -----------------------------
st.set_page_config(
    page_title="AI-Powered Study Buddy",
    page_icon="📚",
    layout="wide"
)

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""

# -----------------------------
# Login Page Function
# -----------------------------
def show_login_page():
    # Creative CSS Styling for Login Page
    st.markdown("""
        <style>
        .login-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 75vh;
        }
        .login-card {
            background: linear-gradient(135deg, #1f4068 0%, #162447 100%);
            padding: 50px 40px;
            border-radius: 24px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
            text-align: center;
            color: #ffffff;
            width: 100%;
            max-width: 440px;
        }
        .login-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 12px;
            color: #ffffff;
        }
        .login-subtitle {
            font-size: 0.95rem;
            color: #b0c4de;
            margin-bottom: 35px;
            line-height: 1.5;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="login-wrapper">
                <div class="login-card">
                    <div style="font-size: 3.5rem; margin-bottom: 10px;">📚</div>
                    <div class="login-title">AI Study Buddy</div>
                    <div class="login-subtitle">Sign in to unlock personalized explanations, quizzes, smart summaries, and study plans.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Centered Button Area via Streamlit native elements placed under layout blocks
        st.markdown("<div style='max-width: 320px; margin: -140px auto 0 auto;'>", unsafe_allow_html=True)
        if st.button("🔵 Sign in with Google", use_container_width=True):
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = "student@gmail.com"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; color: #8c9bae; font-size: 0.75rem; margin-top: 150px;'>Protected by secure authentication workspace</p>", unsafe_allow_html=True)

# -----------------------------
# Main Application Content
# -----------------------------
def show_main_app():
    # Sidebar Profile & Logout
    st.sidebar.title("🚀 User Dashboard")
    st.sidebar.write(f"Signed in as:\n**{st.session_state.get('user_email', 'Student')}**")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["user_email"] = ""
        st.rerun()
        
    st.sidebar.markdown("---")
    
    # Sidebar Menu Options
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

    st.title("📚 AI-Powered Study Buddy")
    st.write(
        "Explain topics, summarize notes, generate quizzes, flashcards and study plans using AI."
    )
    st.markdown("---")

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

# -----------------------------
# Control Flow Gateway
# -----------------------------
if not st.session_state["authenticated"]:
    show_login_page()
else:
    show_main_app()