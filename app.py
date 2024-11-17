import streamlit as st
import google.generativeai as genai
import time
#import firebase_admin
#from firebase_admin import credentials, firestore
from streamlit_option_menu import option_menu
from pages import p_login, p_quiz, p_profile, p_sign_out

from firebase_admin import credentials, firestore, initialize_app

#st.set_page_config(layout='wide')

#st.title("Quizzify - Login")

# Page Configuration
#st.set_page_config(page_title="Smart Quiz Generator", layout="wide")

# Initialize the current page in session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "login"

# Navigation Bar (Only show if not on login page)
if st.session_state["current_page"] != "login":
    selected = option_menu(
        menu_title=None,
        options=["Quiz", "Profile", "Sign Out"],
        icons=["book", "person-bounding-box", "box-arrow-right"],
        orientation="horizontal",
    )

    # Handle navigation based on the selected option
    if selected == "Quiz":
        st.session_state["current_page"] = "quiz"
    elif selected == "Profile":
        st.session_state["current_page"] = "profile"
    elif selected == "Sign Out":
        st.session_state["current_page"] = "login"

# Page Logic
if st.session_state["current_page"] == "login":
    if p_login.login():  # If login is successful, update the page
        st.session_state["current_page"] = "quiz"
elif st.session_state["current_page"] == "quiz":
    p_quiz.quiz()
elif st.session_state["current_page"] == "profile":
    p_profile.profile()
elif st.session_state["current_page"] == "sign_out":
    p_sign_out.sign_out()

genai_api = st.secrets["GEMINI_API"]
sambanova_api = st.secrets["SAMBA_API"]

# Initialize Firestore DB
cred = credentials.Certificate("firebase.json")

# cache the Firebase initialization to avoid reinitializing the app. 
# subsequent calls will return the cached Firestore client.
# Firebase Initialization
# cache the Firebase initialization to avoid reinitializing the app. 
# subsequent calls will return the cached Firestore client.
# Firebase DB setup
@st.cache_resource
def get_firestore():
    return firestore.client()

db = get_firestore()

username = st.text_input("Enter your username")

# # Define available pages
# page = {
#     "Home": "home",
#     "Generate Quiz": "generate_quiz",
#     "Take Quiz": "take_quiz"
# }

# Function to handle page navigation
def go_to_page(page_name):
    st.session_state.page = page_name

# # Create a sidebar
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", list(page.keys()))

# # Page routing based on the selection
# if page == "Home":
#     go_to_page("home")
# elif page == "Generate Quiz":
#     go_to_page("generate_quiz")
# elif page == "Take Quiz":
#     go_to_page("take_quiz")

# if username:
#     st.session_state.username = username
#     st.success(f"Welcome, {username}! Redirecting...")
#     st.success("Successfully logged in! Use the navigation menu to proceed.")
#     st.write("Go to **Home** from the menu.")

# else:
#     st.info("Please fill in all fields to proceed.")
