import streamlit as st
from firebase_admin import firestore
import google.generativeai as genai
import time
import openai

capitalize_sidebar_style = """
    <style>
    [data-testid="stSidebar"] * {
        text-transform: capitalize !important;
    }
    </style>
"""

st.markdown(capitalize_sidebar_style, unsafe_allow_html=True)


# Check for username in session state
if "username" not in st.session_state:
    st.error("Please go back and enter your username.")
    st.switch_page("app.py")  # Redirect to the main page

# Configure Gemini API
genai_api_key = st.secrets["GEMINI_API"]
genai.configure(api_key=genai_api_key)

# Configure SambaNova API
client = openai.OpenAI(
    api_key=st.secrets["SAMBA_API"],
    base_url="https://api.sambanova.ai/v1",
)

# Firebase setup
@st.cache_resource
def get_firestore():
    return firestore.client()

db = get_firestore()

# Get username from session state
username = st.session_state.username

# Streamlit UI
st.title("Prometheus")
st.write("Drop your lectures here to generate quizzes and summaries!")
st.header(f"Hello, {username}! 👋")

# Helper functions
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

        # Wait for processing to complete
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

def generate_quiz(analysis, n=5, difficulty="Medium"):
    try:
        prompt = f"""
        Based on the following analysis, generate {n} quiz questions with difficulty level {difficulty}:
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
            ...
          ]
        }}

        Please only return the JSON without any additional text.
        """
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-8b")
        response = model.generate_content(
            [analysis, prompt], request_options={"timeout": 600}
        )
        return response.text

    except Exception as e:
        return f"Error generating quiz: {e}"

# File upload and processing
st.subheader("Upload a File")
uploaded_file = st.file_uploader("Choose a file", type=["mp4"])

if uploaded_file:
    st.write(f"File uploaded: {uploaded_file.name}")
    st.session_state.uploaded_file_name = uploaded_file.name

    # Firestore reference for the video
    doc_ref = db.collection("users").document(username).collection("videos").document(uploaded_file.name)

    # Check if analysis exists
    existing_data = doc_ref.get()
    if existing_data.exists:
        analysis = existing_data.to_dict().get("analysis")
        st.subheader("Analysis:")
    else:
        with st.spinner("Analyzing video..."):
            transcript = generate_transcript(uploaded_file, uploaded_file.name)
            analysis = generate_analysis(transcript)
            st.subheader("Analysis (Generated):")
            doc_ref.set({"analysis": analysis})

    st.write(analysis)

# Quiz settings
st.subheader("Quiz Settings")
col3, col4 = st.columns(2)
with col3:
    num_questions = st.slider("Number of Questions", min_value=1, max_value=25, value=10)
with col4:
    difficulty = st.selectbox("Difficulty Level", options=["Easy", "Medium", "Hard"], index=1)

if st.button("Take Quiz"):
    if analysis:
        with st.spinner("Generating quiz..."):
            quiz = generate_quiz(analysis, num_questions, difficulty) 
            doc_ref.update({"quiz": quiz}) # Optionally update the quiz in Firestore

        st.session_state.quiz = quiz
        if quiz:
            st.switch_page("pages/Quiz.py")  # Navigate to quiz page
    else:
        st.error("Please upload and analyze a video first.")
