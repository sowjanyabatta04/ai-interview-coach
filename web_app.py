import streamlit as st
import random
from questions import questions
from analyzer import analyze_answer

st.title("AI Interview Coach")

# Session state setup
if "round" not in st.session_state:
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.question_list = []
    st.session_state.category = ""

name = st.text_input("Candidate Name")
category = st.selectbox("Choose Category", ["Python", "HR", "AI"])

# Start Interview
if st.button("Start Interview"):
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.category = category
    st.session_state.question_list = questions[category].copy()
    random.shuffle(st.session_state.question_list)

# Interview flow
if st.session_state.round > 0 and st.session_state.round <= 5:
    st.subheader(f"Round {st.session_state.round}/5")

    question = st.session_state.question_list[st.session_state.round - 1]
    st.write("### Question:")
    st.write(question)

    answer = st.text_area(
       "Your Answer",
       key=f"answer_{st.session_state.round}"
    )

    if st.button("Submit Answer"):
        score, feedback = analyze_answer(question, answer)
        st.session_state.score += score

        st.success(f"Score: {score}/10")
        for item in feedback:
            st.write("- " + item)

        st.session_state.round += 1
        st.rerun()

# Final result
if st.session_state.round > 5:
    avg = st.session_state.score / 5
    st.header("Interview Completed!")
    st.success(f"{name}, Final Score: {avg:.1f}/10")