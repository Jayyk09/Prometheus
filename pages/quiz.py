import streamlit as st
from firebase_admin import firestore

if "username" not in st.session_state:
    st.error("Please go back and enter your username.")
    st.switch_page("app.py")

# Firebase DB setup
@st.cache_resource
def get_firestore():
    return firestore.client()

db = get_firestore()

st.title("Quizz")

# Retrieve username and uploaded file information from session state
username = st.session_state.get("username", "default_user")  # Use default value if not in session state
uploaded_file_name = st.session_state.uploaded_file_name

quiz = st.session_state.quiz
st.write(quiz)

