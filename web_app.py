import streamlit as st

st.title("AI Interview Coach")
st.write("Welcome to your AI Interview Coach website!")

name = st.text_input("Enter Candidate Name")

category = st.selectbox(
    "Choose Category",
    ["Python", "HR", "AI"]
)

if st.button("Start Interview"):
    st.success(f"Welcome {name}! Category: {category}")