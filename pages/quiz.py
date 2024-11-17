import streamlit as st
from firebase_admin import firestore
import time

if "username" not in st.session_state:
    st.error("Please go back and enter your username.")
    st.switch_page("app.py")

# Firebase DB setup
@st.cache_resource
def get_firestore():
    return firestore.client()

db = get_firestore()

st.title("Quizz")

# Retrieve username and uploaded file information from session state
username = st.session_state.get("username", "default_user")  # Use default value if not in session state
uploaded_file_name = st.session_state.uploaded_file_name

quiz = st.session_state.quiz
# print(quiz)
# st.write(quiz)

formatted_quiz = quiz.replace("```json", "").replace("```", "")
print(formatted_quiz)

user_answers = []

if 'page_load_time' not in st.session_state:
    st.session_state.page_load_time = time.time()  # Store page load time when the app starts

# Loop through each question
for i, entry in enumerate(formatted_quiz['quiz']):
    question_text = entry["question_text"]
    options = entry["options"]

    # Display the question and options as radio buttons
    answer = st.radio(question_text, options, key=entry["question_id"], index=None)

    # Store the answer
    user_answers.append(answer)


# Button to submit answers
if st.button("Submit"):
    score = 0
    # Check the answers and calculate the score
    for i, entry in enumerate(formatted_quiz['quiz']):
        if user_answers[i] == entry["correct_option"]:
            score += 1

    button_click_time = time.time()
    st.session_state.time_difference = button_click_time - st.session_state.page_load_time

    st.session_state.score = score
    st.session_state.user_answers = user_answers
    st.session_state.quiz_data = formatted_quiz['quiz']  # Store the entire quiz data
    
    # Show the result
    st.write(f"You got {score} out of {len(formatted_quiz['quiz'])} correct!")
    
    # Display the correct answers and explanations
    for i, entry in enumerate(formatted_quiz['quiz']):
        st.write(f"Q{i+1}: {entry['question_text']}")
        st.write(f"Your answer: {user_answers[i]}")
        st.write(f"Correct answer: {entry['correct_option']}")
        st.write(f"Explanation: {entry['explanation']}")
        st.write("-" * 40)

    st.switch_page('pages/results.py')