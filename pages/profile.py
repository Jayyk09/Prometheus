import streamlit as st
from firebase_admin import firestore
from datetime import datetime

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

# Firebase DB setup
@st.cache_resource
def get_firestore():
    return firestore.client()

db = get_firestore()

st.title("Your Prometheus Dashboard")
username = st.session_state.username
st.sidebar.title("User Profile")
st.sidebar.image("mascot.png", width=125)  # Placeholder profile picture
st.sidebar.markdown(f"""
**Email:** {username}@example.com  
**Role:** Student  
""")

# Fetch quizzes and calculate metrics
videos_ref = db.collection("users").document(username).collection("videos")
videos = [doc.to_dict() for doc in videos_ref.stream()]  # Retrieve all video documents

# Calculate metrics dynamically
quizzes_taken = len([video for video in videos if "quiz_score" in video])  # Count quizzes with scores
total_score = sum(video.get("quiz_score", 0) for video in videos if "quiz_score" in video)
avg_score = round(total_score / quizzes_taken, 2) if quizzes_taken > 0 else 0  # Avoid division by zero
study_hours = len(videos) * 3  # Arbitrary: Assume 3 study hours per video

# Display metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Quizzes Taken", quizzes_taken)
with col2:
    st.metric("Average Score", f"{avg_score}%")
with col3:
    st.metric("Study Hours", study_hours)

st.divider()  # Horizontal rule for better UI separation

# Uploaded files and recent quizzes section
st.header("Uploaded Files and Recent Quizzes")

videos_ref = db.collection("users").document(username).collection("videos")
videos = [
    (
        doc.id,  # Video name
        doc.to_dict().get("quiz_score", "Not Taken"),  # Quiz score
        doc.to_dict().get("quiz"),  # Quiz data
        doc.to_dict().get("difficulty", "Medium"),  # Difficulty level
        doc.create_time,
        doc.to_dict().get("time_taken")  # Upload time
    )
    for doc in videos_ref.stream()
]

# Layout with two sections: Uploaded Files and Recent Quizzes
col1, col2 = st.columns(2)

# Uploaded Files Section
with col1:
    st.subheader("Uploaded Files")
    for video_name,quiz_score,quiz,difficulty, upload_time, _ in videos:
        with st.container():
            st.write(f"📁 **{video_name}**")
            timestamp = upload_time.timestamp()  # Convert to Unix timestamp
            formatted_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            st.caption(f"Uploaded on {formatted_time}")

            if st.button("Take Quiz", key=f"quiz_{video_name}"):  # Unique key for each button
                if quiz:
                    st.session_state["quiz"] = quiz
                    st.session_state["uploaded_file_name"] = video_name
                    st.switch_page("pages/Quiz.py")  # Navigate to the quiz page
                else:
                    st.warning("No quiz data found. Please upload the video and generate a quiz first.")


# Recent Quizzes Section
with col2:
    st.subheader("Recent Quizzes")
    for video_name, quiz_score,_, difficulty,_, time_taken in videos:
        st.markdown(f"**{video_name}**")
        st.progress(int(quiz_score) if quiz_score != "Not Taken" else 0, text=f"{quiz_score}%")
        minutes = int(time_taken // 60)
        seconds = int(time_taken % 60)

        st.caption(f"{minutes} minutes {seconds} seconds • {difficulty}")

