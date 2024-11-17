# # p_quiz.py

# import streamlit as st

# def quiz():
#     st.title("📚 Smart Quiz Generator")
#     st.write("Drop your study materials here or click to browse")
#     st.write("Supports PDF, TXT, and DOCX files")

#     # File Upload Section
#     uploaded_file = st.file_uploader("", type=["pdf", "txt", "docx"], label_visibility="collapsed")

#     # Action Buttons
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("Create Outline"):
#             st.write("Generating structured outline... (Placeholder)")
#     with col2:
#         if st.button("Create Summary"):
#             st.write("Generating summary... (Placeholder)")

#     # Quiz Settings
#     st.subheader("Quiz Settings")
#     col3, col4 = st.columns(2)
#     with col3:
#         num_questions = st.slider("Number of Questions", min_value=1, max_value=25, value=10)
#     with col4:
#         difficulty = st.selectbox("Difficulty Level", options=["Easy", "Medium", "Hard"])

#     # Take Quiz Button
#     if st.button("Take Quiz"):
#         st.write(f"Generating quiz with {num_questions} questions at {difficulty} level...")

import streamlit as st
from firebase_admin import firestore, initialize_app, credentials
import google.generativeai as genai
import time
import openai

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

# Configure Gemini API
genai_api_key = st.secrets["GEMINI_API"]
genai.configure(api_key=genai_api_key)

# Configure Sambanova API
client = openai.OpenAI(
    api_key=st.secrets["SAMBA_API"],
    base_url="https://api.sambanova.ai/v1",
)

@st.cache_resource
def init_firebase():
    cred = credentials.Certificate("firebase.json")
    initialize_app(cred)
    return firestore.client()

db = init_firebase()


# Video Transcript Generation
def generate_transcript(uploaded_file, display_name):
    try:
        file_list = genai.list_files(page_size=100)
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

        prompt = "write transcript of the video"
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-8b")
        response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
        return response.text
    
    except Exception as e:
        return f"Error analyzing video: {e}"

# Analysis Generation
def generate_analysis(transcript):
    try:
        response = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professor analyzing a video transcript and providing a detailed analysis."
                },
                {
                    "role": "user", 
                    "content": f"Analyze the following transcript: {transcript}"
                }
            ],
            temperature=0.1,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating analysis: {e}"

# Quiz Generation
def generate_quiz(analysis, num_questions):
    try:
        prompt = f"""
        Based on the analysis, generate {num_questions} quiz questions in JSON format:
        {{
          "quiz": [
            {{ "question_id": 1, "question_text": "Your question here", "options": ["Option 1", "Option 2", "Option 3", "Option 4"], "correct_option": "Correct option", "explanation": "Explanation here." }},
            ...
          ]
        }}
        """
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-8b")
        response = model.generate_content([analysis, prompt], request_options={"timeout": 600})
        return response.text
    
    except Exception as e:
        return f"Error generating quiz: {e}"

# Main Application
st.title("📚 Smart Quiz Generator")
st.write("Upload study materials or videos to generate analyses, summaries, and quizzes.")

uploaded_file = st.file_uploader("Choose a file", type=["mp4", "pdf", "txt", "docx"])

if uploaded_file:
    st.write(f"File uploaded: {uploaded_file.name}")

    if uploaded_file.name.endswith("mp4"):
        transcript = generate_transcript(uploaded_file, uploaded_file.name)
        analysis = generate_analysis(transcript)

        st.subheader("Analysis:")
        st.write(analysis)

        doc_ref = db.collection("users").document("username").collection("files").document(uploaded_file.name)
        doc_ref.set({"analysis": analysis})

        if st.button("Generate Quiz"):
            num_questions = st.slider("Number of Questions", min_value=1, max_value=25, value=10)
            quiz = generate_quiz(analysis, num_questions)
            st.subheader("Generated Quiz:")
            st.json(quiz)
            doc_ref.update({"quiz": quiz})
    else:
        st.write("File type not supported for transcript analysis.")
