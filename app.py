import streamlit as st
import google.generativeai as genai
import time
# import firebase_admin
# from firebase_admin import credentials, firestore

st.write("Welcome to Quizzify")
st.text_input("Enter Username:")


if st.button('Go to Login Page'):
    st.switch_page("pages/login.py")
