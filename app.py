import streamlit as st
import google.generativeai as genai
import time
#import firebase_admin
#from firebase_admin import credentials, firestore
from streamlit_option_menu import option_menu
from pages import p_login, p_quiz, p_profile, p_sign_out

# Page Configuration
st.set_page_config(page_title="Smart Quiz Generator", layout="wide")

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