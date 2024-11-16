import streamlit as st

st.set_page_config(
    page_title="Login App"
)

# st.title("Login")

if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Home page button
if st.session_state.page == 'login':
    st.title("Login Page")
    if st.button('Go to Home Page'):
        st.session_state.page = 'home'