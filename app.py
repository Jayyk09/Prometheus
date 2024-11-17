import streamlit as st
import google.generativeai as genai
import time
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(layout='wide')

st.title("Quizzify - Login")

genai_api = st.secrets["GEMINI_API"]
sambanova_api = st.secrets["SAMBA_API"]

# Initialize Firestore DB
cred = credentials.Certificate("firebase.json")

# cache the Firebase initialization to avoid reinitializing the app. 
# subsequent calls will return the cached Firestore client.
@st.cache_resource
def init_firebase():
    cred = credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

username = st.text_input("Enter your username")

# Define available pages
page = {
    "Home": "home",
    "Generate Quiz": "generate_quiz",
    "Take Quiz": "take_quiz"
}

# Function to handle page navigation
def go_to_page(page_name):
    st.session_state.page = page_name

# # Create a sidebar
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", list(page.keys()))

# Page routing based on the selection
if page == "Home":
    go_to_page("home")
elif page == "Generate Quiz":
    go_to_page("generate_quiz")
elif page == "Take Quiz":
    go_to_page("take_quiz")

if username:
    st.session_state.username = username
    st.success(f"Welcome, {username}! Redirecting...")
    st.success("Successfully logged in! Use the navigation menu to proceed.")
    st.write("Go to **Home** from the menu.")

else:
    st.info("Please fill in all fields to proceed.")
