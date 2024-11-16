import streamlit as st
import google.generativeai as genai
import time
import firebase_admin
from firebase_admin import credentials, firestore

st.title('Quizzify')

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
    # Show the list of videos with the video name that the user has uploaded
    videos_ref = db.collection("users").document(username).collection("videos")
    videos = [doc.id for doc in videos_ref.stream()]
    if videos:
        st.write("Uploaded videos:")
        for video in videos:
            if st.button(video):  # Create a button for each video
                st.session_state.video_to_show = video  # Store the selected video in session state
                st.rerun()  # Rerun the app to go to the new page
    else:
        st.write("No videos uploaded yet.")