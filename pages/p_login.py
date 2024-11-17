# p_login.py
import streamlit as st

def login():
    st.title("🔒 Login")
    st.write("Please enter your credentials to log in.")

    # Input Fields for Login
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login Button
    if st.button("Login"):
        if username == "admin" and password == "password":  # Replace with real auth logic
            st.success("Login successful! Redirecting to the Quiz page...")
            return True
        else:
            st.error("Invalid username or password!")
    return False