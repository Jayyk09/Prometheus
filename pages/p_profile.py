import streamlit as st

def profile():
    st.title("👤 Profile")
    st.write("Here is your profile page.")
    st.write("Name: John Doe")
    st.write("Email: john.doe@example.com")
    if st.button("Edit Profile"):
        st.write("Profile editing not implemented yet!")