import streamlit as st
from firebase_admin import firestore
import time
import json

capitalize_sidebar_style = """
    <style>
    [data-testid="stSidebar"] * {
        text-transform: capitalize !important;
    }
    </style>
"""

st.markdown(capitalize_sidebar_style, unsafe_allow_html=True)

if "username" not in st.session_state:
    st.error("Please go back and enter your username.")
    st.switch_page("app.py")

# Check if a file has been uploaded
if "uploaded_file_name" not in st.session_state:
    st.error("Please go back and upload a file.")
    st.switch_page("pages/Home.py")

# Firebase DB setup
@st.cache_resource
def get_firestore():
    return firestore.client()

db = get_firestore()

st.title("Prometheus Quizz")

# Retrieve username and uploaded file information from session state
username = st.session_state.get("username", "default_user")  # Use default value if not in session state
uploaded_file_name = st.session_state.uploaded_file_name

# write the file name
st.write(f"Quiz for: {uploaded_file_name}")

quiz = st.session_state.quiz
formatted_quiz = json.loads(quiz.replace("```json", "").replace("```", ""))

# Initialize user answers in session_state if it doesn't exist yet
user_answers= []

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
    incorrect_answers = []  # List to store incorrect answers

    # Check the answers and calculate the score
    for i, entry in enumerate(formatted_quiz['quiz']):
        if user_answers[i] == entry["correct_option"]:
            score += 1
        else:
            incorrect_answers.append((i, entry))  # Store incorrect answer details


    button_click_time = time.time()
    st.session_state.time_difference = button_click_time - st.session_state.page_load_time

    st.session_state.score = score
    st.session_state.user_answers = user_answers
    st.session_state.quiz_data = formatted_quiz['quiz']  # Store the entire quiz data
    
    # Show the result
    st.write(f"You got {score} out of {len(formatted_quiz['quiz'])} correct!")
    
    # Display the correct answers and explanations
    if incorrect_answers:
        st.write("### Here's a breakdown of the questions you missed:")

        # Scrollable container with custom style
        container_style = """
        <style>
            .card {
                margin-bottom: 20px;
                padding: 15px;
                border: 1px solid #2196F3;
                border-radius: 10px;
            }
            .question-title {
                font-weight: bold;
                color: #0D47A1;
            }
            .answer {
                color: #d32f2f;
            }
            .correct {
                color: #388E3C;
            }
            .explanation {
                color: #6A1B9A;
            }
        </style>
        """

        st.markdown(container_style, unsafe_allow_html=True)

        # Content inside the scrollable container
        st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
        for idx, entry in incorrect_answers:
            question_text = entry["question_text"]
            correct_option = entry["correct_option"]
            explanation = entry["explanation"]
            user_answer = user_answers[idx - 1]  # Map user answer by index (adjusted for 0-based indexing)

            card_html = f"""
            <div class="card">
                <p class="question-title">Q{idx}: {question_text}</p>
                <p><span class="answer">Your answer:</span> {user_answer}</p>
                <p><span class="correct">Correct answer:</span> {correct_option}</p>
                <p><span class="explanation">Explanation:</span> {explanation}</p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.success("Congratulations! You answered all questions correctly!")
    
    # Store the quiz score in percentage and user answers in Firestore
    doc_ref = db.collection("users").document(username).collection("videos").document(uploaded_file_name)
    doc_ref.update({
        "quiz_score": round((score / len(formatted_quiz['quiz'])) * 100, 2),
        "time_taken": round(st.session_state.time_difference, 2)
    })