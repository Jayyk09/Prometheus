# p_login.py
import streamlit as st

def login():
    st.title("🔒 Login")
    st.write("Please enter your credentials to log in.")

    # Input Fields for Login
    username = st.text_input("Username")

    # Login Button
    if st.button("Login"):
        st.success("Login successful! Redirecting to the Quiz page...")
        return True
    return False