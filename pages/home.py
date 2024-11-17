import streamlit as st
from firebase_admin import firestore
import google.generativeai as genai
import time
import openai

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

# Get username from session state
if "username" not in st.session_state:
    st.error("Please go back and enter your username.")
    st.switch_page("app.py")


# configure Gemini API
genai_api_key = st.secrets["GEMINI_API"]
genai.configure(api_key=genai_api_key)

# configure Sambanova API
client = openai.OpenAI(
    api_key=st.secrets["SAMBA_API"],
    base_url="https://api.sambanova.ai/v1",
)

username = st.session_state.username

st.title("Quizzify")
st.write("Drop your lectures here to generate quizzes and summaries!")

# Welcome message
st.header(f"Hello, {username}! 👋")

# Firebase DB setup
@st.cache_resource
def get_firestore():
    return firestore.client()

db = get_firestore()

# Analyze video
def generate_transcript(uploaded_file, display_name):
    try:
        # Get file list in Gemini
        file_list = genai.list_files(page_size=100)

        # Check if the file is already uploaded
        video_file = next((f for f in file_list if f.display_name == display_name), None)

        if video_file is None:
            video_file = genai.upload_file(
                path=uploaded_file, 
                display_name=display_name,
                mime_type="video/mp4",
                resumable=True
            )

        while video_file.state.name == "PROCESSING":
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError("File processing failed.")

        # Generate content using the uploaded file
        prompt = "write transcript of the video"
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-8b")
        response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
        return response.text
    
    except Exception as e:
        return f"Error analyzing video: {e}"

# Function to generate analysis
def generate_analysis(transcript):
    try:
        response = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professor analyzing a video transcript and providing a detailed analysis of the material. Summarize the key points of the transcript, including the main themes, important arguments, and conclusions. Focus on giving a clear and concise understanding of the content."
                },
                {
                    "role": "user", 
                    "content": f"Analyze the following transcript and provide a detailed summary, highlighting the key themes, arguments, and conclusions: {transcript}. The response should be in a clear, structured format."
                }
            ],
            temperature=0.1,
            max_tokens=500
        )
        analysis = response.choices[0].message.content
        return analysis
    
    except Exception as e:
        return f"Error generating analysis: {e}"

# Function to generate quiz
def generate_quiz(analysis, n =5, difficulty="Medium"):
    """
    This function generates quiz questions using the Gemini Pro 1.5 model based on the analysis of the video.
    Args:
      analysis: The analysis of the video.
      n: The number of quiz questions to generate.

    Returns:
      A string with the generated quiz questions in JSON format.
    """
    try:
        # Prepare the request to generate the quiz questions
        prompt = f"""
        Based on the following analysis, generate {n} quiz questions with diffulty level {difficulty}:
        Return the quiz in the following JSON format:

        {{
          "quiz": [
            {{ 
              "question_id": 1,
              "question_text": "Your question here",
              "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4"
              ],
              "correct_option": "Correct option here",
              "explanation": "Explanation for the correct answer."
            }},
            {{
              "question_id": 2,
              "question_text": "Your question here",
              "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4"
              ],
              "correct_option": "Correct option here",
              "explanation": "Explanation for the correct answer."
            }},
            ...
            {{ 
              "question_id": {n},
              "question_text": "Your question here",
              "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4"
              ],
              "correct_option": "Correct option here",
              "explanation": "Explanation for the correct answer."
            }}
          ]
        }}

        Please only return the JSON without any additional text.
        """

        # Generate quiz using Gemini
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-8b")
        response = model.generate_content(
            [analysis, prompt], request_options={"timeout": 600}
        )

        # Return the generated quiz questions in JSON format
        return response.text 
    
    except Exception as e:
        return f"Error generating quiz: {e}"

# File upload
st.subheader("Upload a File")
uploaded_file = st.file_uploader("Choose a file", type=["mp4"])
if uploaded_file:
    st.write(f"File uploaded: {uploaded_file.name}")
    st.session_state.uploaded_file_name = uploaded_file.name

    # Analyze the video
    transcript = generate_transcript(uploaded_file, uploaded_file.name)
    analysis = generate_analysis(transcript)
    st.subheader("Analysis:")
    st.write(analysis)
    doc_ref = db.collection("users").document(username).collection("videos").document(uploaded_file.name)
    doc_ref.set({
        "analysis": analysis
    })

st.subheader("Quiz Settings")
col3, col4 = st.columns(2)
with col3:
    num_questions = st.slider("Number of Questions", min_value=1, max_value=25, value=10)
with col4:
    difficulty = st.selectbox("Difficulty Level", options=["Easy", "Medium", "Hard"], index=1)


# Button to generate quiz
if st.button("Take Quiz"):
    if analysis:
        quiz = generate_quiz(analysis, num_questions, difficulty)
    else:
        quiz = "No analysis found. Please upload a video and generate analysis first."
    doc_ref.update({
        "quiz": quiz
    })
    st.session_state.quiz = quiz
    if quiz:
        st.switch_page("pages/quiz.py")