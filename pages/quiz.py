import streamlit as st
import json

st.set_page_config(
    page_title="Quiz Page"
)

data = [
    {
        "question": "What is the speaker's favorite argument for the existence of God?",
        "options": [
            "The argument from design",
            "The cosmological argument",
            "The moral argument",
            "The ontological argument"
        ],
        "answer": "The cosmological argument"
    },
    {
        "question": "What is the first premise of the cosmological argument as presented in the video?",
        "options": [
            "The universe is infinitely old.",
            "Everything that exists has a cause.",
            "Whatever begins to exist has a cause.",
            "God is the unmoved mover."
        ],
        "answer": "Whatever begins to exist has a cause."
    },
    {
        "question": "According to the speaker, what kind of evidence supports the idea that the universe had a beginning?",
        "options": [
            "Philosophical arguments only",
            "Scientific evidence only",
            "Both philosophical arguments and scientific evidence",
            "None of the above"
        ],
        "answer": "Both philosophical arguments and scientific evidence"
    }
]

css = """
<style>
    .quiz-box {
        border: 3px solid #4CAF50;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-bottom: 30px;
    }
    .question-box {
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #fff;
    }
    .answer-box {
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stRadio {
        border: 1px solid #ddd;
        border-radius: 5px;
    }
</style>
"""

# Inject custom CSS
st.markdown(css, unsafe_allow_html=True)

st.title("Multiple Choice Quiz")

# To store the user's answers
user_answers = []

# Box around the entire quiz
with st.container():
    st.markdown('<div class="quiz-box">', unsafe_allow_html=True)

    # Loop through each question
    for i, entry in enumerate(data):
        question = entry["question"]
        options = entry["options"]

        # Box around each question
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        answer = st.radio(question, options, key=i, label_visibility="visible")
        st.markdown('</div>', unsafe_allow_html=True)

        # Store the answer
        user_answers.append(answer)

    # Button to submit answers
    if st.button("Submit"):
        score = 0
        # Check the answers and calculate the score
        for i, entry in enumerate(data):
            if user_answers[i] == entry["answer"]:
                score += 1
        
        # Show the result
        st.write(f"You got {score} out of {len(data)} correct!")

        # Display the correct answers
        for i, entry in enumerate(data):
            st.write(f"Q{i+1}: {entry['question']}")
            st.write(f"Your answer: {user_answers[i]}")
            st.write(f"Correct answer: {entry['answer']}")
            st.write("-" * 40)

    st.markdown('</div>', unsafe_allow_html=True)  # Close the quiz box