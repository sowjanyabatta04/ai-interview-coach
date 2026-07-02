import streamlit as st
import random
from questions import questions
from analyzer import analyze_answer
from streamlit_autorefresh import st_autorefresh
from reportlab.pdfgen import canvas
import os

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

st.title("AI Interview Coach")

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
resume = st.file_uploader("Upload Resume (PDF/TXT)",type=["pdf", "txt"])
resume_text = ""
if resume is not None:
    resume_text = resume.read().decode("utf-8")
    st.success("Resume uploaded successfully!")
category = st.selectbox("Choose Category", ["Python", "HR", "AI"])

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
            score, feedback = analyze_answer(question, answer)
            st.session_state.score += score
            st.session_state.feedback = (score, feedback)
            st.session_state.answer_submitted = True

    # Show Feedback
    if st.session_state.feedback:
        score, feedback = st.session_state.feedback

        st.success(f"Score: {score}/10")
        st.write("### Feedback:")
        for item in feedback:
            st.write("- " + item)

        # Final result after round 5
        if st.session_state.round == 5:
            avg = st.session_state.score / 5
            st.header("Interview Completed!")
            st.success(f"{name}, Final Score: {avg:.1f}/10")

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