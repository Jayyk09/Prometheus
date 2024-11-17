# Prometheus - Your Personal Study Assistant

Prometheus is an AI-powered tool that generates notes, summaries, and quizzes from both text and video inputs. The platform provides users with personalized content based on their uploads, allowing them to learn and review material effectively.

## Features

- **Multiple Format Support:** Upload text files or videos (MP4) for analysis.
- **Notes & Summary Generation:** AI extracts key points and creates detailed lecture notes with timestamps.
- **Quiz Generation:** Automatically generates multiple-choice quizzes with varying difficulty.
- **User Authentication:** Create a profile to track quiz results, notes, and progress.
- **Review Reminders:** Get reminders to review quizzes and material after a set period.
- **Persistent Account Data:** Access your saved notes, quizzes, and results anytime.

## How It Works

1. **Upload Content:** 
   - Users can upload videos via the web interface.
   
2. **AI Analysis:**
   - Prometheus uses powerful AI models to process the content:
     - For text, it generates summaries, outlines, and quizzes.
     - For video, it extracts key moments and timestamps to create lecture notes.

3. **Quiz & Review:**
   - Based on the content, quizzes are generated. Users can take the quiz, check their answers, and get suggestions for areas to review.

4. **User Profiles:**
   - Track your progress with personalized accounts. Review uploaded files, quizzes, and get reminders based on your learning patterns.

## Technologies Used

- **Streamlit:** For building the interactive web interface.
- **AI Models (SambaNova/Gemini):** For analyzing teext and video content to generate summaries and quizzs.
- **Firebase:** For user authentication, storage of results, and persistent data management.
- **Python:** Backend support for content processing and API management.
- 

## Getting Started

1. **Clone the repository:** `git clone https://github.com/your-username/notewise.git`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Set up Firebase:**
   - Create a Firebase project and obtain your credentials file (`firebase-credentials.json`).
   - Replace `"path/to/your/firebase.json"` in the code with the actual path to your credentials file.
4. **Configure Gemini API key:**
   - Obtain a Gemini API key from Google Cloud.
   - Create a `secrets.toml` file in the `.streamlit` directory and add your API key:
     ```toml
     [secrets]
     GEMINI_API = "your_actual_api_key_here"
     ```
5. **Configure SambaNova API key:**
    - Obtain the API key from SambaNova and put it the `secrets.toml` file in the `.streamlit` directory.
    ```SAMBA_API = "your_actual_api_key_here"```

6. **Run the app:** `streamlit run app.py`

## Future Enhancements

- **User Authentication:** Implement a robust user authentication system using Firebase Authentication.
- **Review Notes:** Add features to review notes
- **Multi-format Support:** Add support for analyzing and generating notes from docx, pdf and audio files.
- 

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License
