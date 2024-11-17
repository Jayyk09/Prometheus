import streamlit as st
import google.generativeai as genai
import time
import firebase_admin
from firebase_admin import credentials, firestore

capitalize_sidebar_style = """
    <style>
    [data-testid="stSidebar"] * {
        text-transform: capitalize !important;
    }
    </style>
"""

st.markdown(capitalize_sidebar_style, unsafe_allow_html=True)


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

if username:
    st.session_state.username = username
    st.success(f"Welcome, {username}! Please proceed to the home page.")
    st.switch_page("pages/Home.py")

else:
    st.info("Please fill in all fields to proceed.")
