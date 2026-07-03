import streamlit as st
import random
from questions import questions
from analyzer import analyze_answer
from streamlit_autorefresh import st_autorefresh
from reportlab.pdfgen import canvas
import os
from PyPDF2 import PdfReader
from docx import Document

col1, col2, col3 = st.columns([4,1.35,4])

with col2:
    st.image("logo.jpg", width=150)

st.markdown("""
<h2 style='text-align: center; color: white; margin-bottom: 5px;'>
Welcome!
</h2>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
}

h1, h2, h3 {
    color: #00ffd5 !important;
    text-align: center;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button {
    background: linear-gradient(90deg, #4A00E0, #8E2DE2);
    color: white;
    border: none;
}
.stTextInput input, .stTextArea textarea {
    border-radius: 12px;
}

[data-testid="stFileUploader"] {
    background-color: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

def get_resume_questions(text):
    questions = []

    text = text.lower()

    if "python" in text:
        questions.append("You mentioned Python. Explain list vs tuple.")

    if "machine learning" in text:
        questions.append("You mentioned ML. What is overfitting?")

    if "ai" in text:
        questions.append("What AI projects have you built?")

    if "streamlit" in text:
        questions.append("Explain your Streamlit project.")

    return questions

def generate_pdf(name, category, score):
    filename = "report.pdf"

    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 16)
    c.drawString(180, 800, "AI Interview Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Candidate Name: {name}")
    c.drawString(50, 720, f"Category: {category}")
    c.drawString(50, 690, f"Final Score: {score:.1f}/10")

    if score >= 8:
        result = "Excellent"
    elif score >= 6:
        result = "Good"
    elif score >= 4:
        result = "Average"
    else:
        result = "Needs Improvement"

    c.drawString(50, 660, f"Performance: {result}")

    c.drawString(50, 620, "Feedback:")
    c.drawString(70, 590, "- Continue practicing interviews")
    c.drawString(70, 560, "- Improve confidence and communication")
    c.drawString(70, 530, "- Give detailed answers with examples")

    c.save()
    return filename

st.markdown("""
<h1 style='text-align:center;
           color:#00ffd5;
           margin-top:3px;
           margin-bottom:0px;'>
🤖 AI Interview Coach
</h1>
<p style='text-align:center;font-size:20px;color:#dddddd;'>
Practice interviews like a real candidate
</p>
""", unsafe_allow_html=True)


# Session state setup
if "round" not in st.session_state:
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.question_list = []
    st.session_state.category = ""
    st.session_state.feedback = None
    st.session_state.answer_submitted = False

if "time_left" not in st.session_state:
    st.session_state.time_left = 60


name = st.text_input("Candidate Name")
resume = st.file_uploader(
    "",
    type=["pdf", "txt", "docx"])

resume_text = ""

if resume is not None:
    file_name = resume.name.lower()

    # TXT
    if file_name.endswith(".txt"):
        resume_text = resume.read().decode("utf-8")

    # PDF
    elif file_name.endswith(".pdf"):
        pdf_reader = PdfReader(resume)

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

    # DOCX
    elif file_name.endswith(".docx"):
        doc = Document(resume)

        for para in doc.paragraphs:
            resume_text += para.text + "\n"

    st.success("Resume uploaded successfully!")
category = st.selectbox("Choose Category", ["Python", "HR", "AI"])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Questions", "5")

with col2:
    st.metric("Time / Question", "60s")

with col3:
    st.metric("Mode", "AI")

# Start Interview
if st.button("Start Interview"):
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.category = category
    resume_questions = get_resume_questions(resume_text)

    remaining = 5 - len(resume_questions)

    if remaining < 0:
        remaining = 0

    normal_questions = random.sample(
        questions[category],
        remaining
    )

    st.session_state.question_list = (
         resume_questions + normal_questions
    )
    random.shuffle(st.session_state.question_list)
    st.session_state.feedback = None
    st.session_state.answer_submitted = False
    st.session_state.time_left = 60


# Interview flow
if 0 < st.session_state.round <= 5:
    st.subheader(f"Round {st.session_state.round}/5")

    progress = st.session_state.round / 5
    st.progress(progress)

    # Timer runs only if answer not submitted
    if not st.session_state.answer_submitted:
        st_autorefresh(interval=1000, key="timer_refresh")
        st.session_state.time_left -= 1

        if st.session_state.time_left < 0:
            st.session_state.time_left = 0

    st.warning(f"⏳ Time Left: {st.session_state.time_left} sec")

    question = st.session_state.question_list[
        st.session_state.round - 1
    ]

    st.write("### Question:")
    st.write(question)

    answer = st.text_area(
        "Your Answer",
        key=f"answer_{st.session_state.round}"
    )

    # Auto timeout
    if st.session_state.time_left == 0 and not st.session_state.answer_submitted:
        st.error("Time Up!")
        st.session_state.feedback = (
            0,
            ["Time over. No answer submitted."]
        )
        st.session_state.answer_submitted = True

    # Submit Answer
    if not st.session_state.answer_submitted:
         if st.button("Submit Answer"):

             with st.spinner("AI is analyzing your answer..."):
                  score, feedback = analyze_answer(question, answer)

             st.session_state.score += score
             st.session_state.feedback = (score, feedback)
             st.session_state.answer_submitted = True

    # Show Feedback
    if st.session_state.feedback:
        score, feedback = st.session_state.feedback

        st.markdown(f"""
        <div style='background:#1f2937;padding:20px;border-radius:15px;text-align:center;'>
        <h2 style='color:#00ff99;'>Score: {score}/10</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write("### Feedback:")
        for item in feedback:
            st.write("- " + item)

        # Final result after round 5
        if st.session_state.round == 5:
            avg = st.session_state.score / 5
            st.balloons()
            if avg >= 9:
                label = "🏆 Excellent"
            elif avg >= 7:
                label = "🟢 Good"
            elif avg >= 4:
                label = "🟡 Average"
            else:
                label = "🔴 Needs Improvement"

            st.markdown(f"""
            <div style='background:#111827;
                        padding:30px;
                        border-radius:20px;
                        text-align:center;
                        margin-top:20px;'>
                  <h1 style='color:#00ffd5;'>Interview Completed 🎉</h1>
                  <h2 style='color:white;'>Candidate: {name}</h2>
                  <h2 style='color:#00ff99;'>Final Score: {avg:.1f}/10</h2>
                  <h2>{label}</h2>
            </div>
            """, unsafe_allow_html=True)

            st.caption("Built by Sowjanya | AI Interview Coach © 2026")

            pdf_file = generate_pdf(name, category, avg)

            with open(pdf_file, "rb") as file:
                st.download_button(
                  label="Download Report PDF",
                  data=file,
                  file_name="AI_Interview_Report.pdf",
                  mime="application/pdf"
            )

        else:
            if st.button("Next Question"):
                st.session_state.round += 1
                st.session_state.feedback = None
                st.session_state.answer_submitted = False
                st.session_state.time_left = 60
                st.rerun()