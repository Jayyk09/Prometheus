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

st.title("👤 Profile")
st.write("Here is your profile page.")
username = st.session_state.username
st.write(f"Name: {username}")

# Get user's videos
videos_ref = db.collection("users").document(username).collection("videos")
videos = [doc.id for doc in videos_ref.stream()]
st.title("Videos")
for i, video in enumerate(videos):
    st.write(f"{i+1}. {video}")
