from PyPDF2 import PdfReader
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components

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
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="AI-Powered Study Buddy",
    page_icon="📚",
    layout="wide"
)

# Initialize Session States
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""

# -----------------------------
# Animated Login Page Gateway
# -----------------------------
def show_login_page():
    # Read the custom HTML animation file
    try:
        with open("loginpage.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=580, scrolling=False)
    except Exception:
        st.error("Could not load loginpage.html template. Make sure it is in the root directory.")

    # Streamlit fallback trigger button for session toggle matching UI action
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔓 Click Here to Bypass/Simulate Successful Login", use_container_width=True):
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = "student@ai-study.com"
            st.rerun()

# -----------------------------
# Main Application Dashboard
# -----------------------------
def show_main_app():
    # Sidebar Profile & Logout Option
    st.sidebar.title("🚀 Student Dashboard")
    st.sidebar.write(f"Logged in as:\n**{st.session_state.get('user_email', 'Student')}**")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["user_email"] = ""
        st.rerun()
        
    st.sidebar.markdown("---")
    
    # Updated Sidebar Menu including Extra-Curricular & Career Advisor
    option = st.sidebar.selectbox(
        "Choose Feature",
        [
            "Explain Topic",
            "PDF Summarizer",
            "Quiz Generator",
            "Flashcard Generator",
            "Study Plan Generator",
            "Extra-Curricular & Career Coach"  # <--- Newly Added Feature
        ]
    )

    st.title("📚 AI-Powered Study Buddy")
    st.write(
        "Explain topics, summarize notes, generate quizzes, flashcards, study plans, and extra-curricular growth guidance using AI."
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
                            f"Explain {topic} in simple language. Give examples. Include key points."
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
        uploaded_file = st.file_uploader("Upload PDF Notes", type=["pdf"])
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
                            f"Summarize these notes into easy bullet points:\n\n{text[:10000]}"
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
                            f"Create 10 multiple choice questions on {topic}. Provide answers at the end."
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
                            f"Create 10 flashcards on {topic}.\n\nFormat:\nQuestion:\nAnswer:"
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
        days = st.number_input("Days Left For Exam", min_value=1, max_value=100, value=15)
        if st.button("Generate Study Plan"):
            if subject:
                try:
                    with st.spinner("Creating Study Plan..."):
                        response = model.generate_content(
                            f"Create a detailed {days}-day study plan for {subject}. Divide topics day-wise. Include: - Daily goals - Revision schedule - Practice tests"
                        )
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter a subject.")

    # ==================================================
    # 6. Extra-Curricular & Career Coach (NEW FEATURE)
    # ==================================================
    elif option == "Extra-Curricular & Career Coach":
        st.header("🌟 Extra-Curricular & Career Development Coach")
        st.write("Get AI recommendations for hackathons, technical clubs, certifications, soft-skill projects, and internship readiness roadmaps tailored for tech students.")
        
        domain = st.selectbox(
            "Select Your Area of Interest / Domain",
            ["Software & Web Development", "Artificial Intelligence & ML", "Core Computer Science & DSA", "Open Source & Hackathons", "General Professional Growth"]
        )
        
        goal = st.text_input("Enter your current focus/goal (e.g., Preparing for summer internships, building resume projects)")
        
        if st.button("Generate Growth Roadmap"):
            try:
                with st.spinner("Analyzing profile requirements and building coaching strategy..."):
                    response = model.generate_content(
                        f"""
                        Act as an elite university career coach for a Computer Science engineering student.
                        Domain: {domain}
                        Student Goal: {goal}
                        
                        Provide a practical, structured extra-curricular and professional growth strategy including:
                        1. Recommended Technical Hackathons or Contests to participate in.
                        2. Open-source or Portfolio Project ideas that stand out to recruiters.
                        3. Essential Certifications or Skill Milestones.
                        4. Soft skills & Group Discussion communication tips.
                        """
                    )
                st.success("Your Custom Career & Extra-Curricular Roadmap is Ready!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

# -----------------------------
# Control Flow Gate
# -----------------------------
if not st.session_state["authenticated"]:
    show_login_page()
else:
    show_main_app()