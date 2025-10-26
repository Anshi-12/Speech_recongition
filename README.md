# VoiceScribe - Advanced Speech Recognition Web Application

VoiceScribe is a powerful web application that transforms audio recordings into accurate text transcriptions using cutting-edge AI technology. Built with Flask, Bootstrap, and the Wav2Vec 2.0 speech recognition model, this application offers a seamless experience for converting spoken content into written text with intelligent Q&A capabilities.

## 🚀 Features

- **AI-Powered Transcription**: Uses Facebook's Wav2Vec 2.0 Large model for accurate speech recognition
- **Intelligent Q&A System**: Ask questions about your transcribed content using DistilBERT AI model
- **Multiple Audio Formats**: Support for MP3, WAV, M4A, FLAC, and OGG audio files
- **User Authentication**: Secure login and registration system
- **Dashboard**: Personalized user dashboard with transcription history and Q&A statistics
- **File Management**: Upload, view, and manage audio transcriptions
- **Q&A History**: Save and review all your questions and AI-generated answers
- **Confidence Scoring**: Get confidence ratings for AI answers
- **Suggested Questions**: Automatically generated relevant questions based on content
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Copy & Download**: Easily copy or download transcription results

## 📋 Technical Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Backend**: Python, Flask
- **Database**: SQLAlchemy with Flask-Migrate
- **Authentication**: Flask-Login
- **AI Models**: 
  - Wav2Vec 2.0 (Speech Recognition)
  - DistilBERT-base-cased-distilled-squad (Question Answering)
- **ML Libraries**: PyTorch, Transformers, Sentence-Transformers
- **Audio Processing**: Librosa, PyDub, SpeechRecognition
- **Styling**: Font Awesome icons, Animate.css animations

## 🛠️ Project Structure

```
speech_recognition/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   ├── templates/
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard/
│   │   │   ├── index.html
│   │   │   ├── history.html
│   │   │   └── view_recording.html
│   │   ├── transcribe/
│   │   │   ├── index.html
│   │   │   └── result.html
│   │   ├── qa/
│   │   │   ├── index.html
│   │   │   └── history.html
│   │   ├── partials/
│   │   │   └── navbar.html
│   │   ├── about.html
│   │   ├── base.html
│   │   └── index.html
│   ├── services/
│   │   └── qa_service.py
│   ├── models/
│   │   ├── user.py
│   │   ├── recording.py
│   │   └── qa_session.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── speech.py
│   │   ├── transcribe.py
│   │   └── qa.py
│   ├── __init__.py
│   └── config.py
├── migrations/
├── setup_qa_feature.py
├── QA_FEATURE_README.md
└── requirements.txt
```

## 📌 Key Pages

- **Home Page**: Introduction to VoiceScribe with feature highlights
- **Dashboard**: User dashboard showing statistics and recent transcriptions
- **Transcribe**: Upload audio files for transcription
- **Q&A Interface**: Ask questions about your transcribed content
- **History**: View and manage all past transcriptions and Q&A sessions
- **Profile**: User account management
- **About**: Information about the application and technology

## 🔧 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/speech_recognition.git
   cd speech_recognition
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the Q&A feature (optional but recommended):
   ```bash
   python setup_qa_feature.py
   ```

5. Set up environment variables:
   ```bash
   # Windows
   set FLASK_APP=app
   set FLASK_ENV=development
   
   # macOS/Linux
   export FLASK_APP=app
   export FLASK_ENV=development
   ```

6. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

7. Run the application:
   ```bash
   python run.py
   ```

8. Open your browser and navigate to `http://127.0.0.1:5000`

## 📱 Usage Guide

1. **Create an Account**: Register with a username, email, and password
2. **Login**: Access your personalized dashboard
3. **Upload Audio**: Navigate to the transcribe page and upload an audio file
4. **View Results**: See the transcription result and copy or download the text
5. **Ask Questions**: Click "Ask Questions" to use the AI Q&A feature about your transcript
6. **Review Q&A History**: Access all your questions and answers from the Q&A history page
7. **Manage History**: Access all your past transcriptions from the history page

## 🤖 Q&A Feature

The intelligent Q&A system allows you to ask questions about your transcribed content:

- **Smart Answers**: Uses DistilBERT AI model trained on SQuAD dataset
- **Confidence Scores**: See how confident the AI is about each answer
- **Suggested Questions**: Get automatically generated relevant questions
- **Source Attribution**: See which part of the transcript the answer came from
- **History Tracking**: All Q&A sessions are saved for future reference

### Example Questions:
- "What was the main topic discussed?"
- "When did this event happen?"
- "Who was mentioned in the conversation?"
- "What was the conclusion reached?"

## 💡 Tips for Best Results

- **Audio Quality**: Higher quality audio files result in more accurate transcriptions
- **Clear Speech**: Speak clearly and at a moderate pace
- **File Size**: Files under 10MB work best. For longer recordings, consider splitting into smaller segments
- **Processing Time**: Transcription typically takes 10-60 seconds depending on the length of your audio file
- **Q&A Questions**: Be specific and use keywords from the transcript for better answers
- **First Q&A**: The first question may take longer as the AI model downloads (~250MB)

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/6957ac91-5069-4e1a-a0dc-688b665d0044)
![image](https://github.com/user-attachments/assets/12081d62-5c35-4f78-8065-4511a0493e43)
![image](https://github.com/user-attachments/assets/615e0308-ad15-4d18-8971-79865dcfeeed)
![image](https://github.com/user-attachments/assets/0b2d8821-97fa-45c8-85b0-02f8feda9002)
![image](https://github.com/user-attachments/assets/daeb9a8f-3ea5-4553-94fa-8046a5506aef)

## 🔒 Security Features

- Secure user authentication
- Password hashing
- CSRF protection
- Private transcription storage
- Session management
- Local AI processing (no external API calls for Q&A)

## 🌟 Future Enhancements

- Real-time transcription
- Speaker diarization (multi-speaker detection)
- Additional language support
- Advanced editing tools
- Team collaboration features
- API access
- Multi-language Q&A support
- Voice-based Q&A queries

## 📄 License

[Your License Information]

## 📞 Contact

For questions, suggestions, or support:
- Email: support@voicescribe.com
- [Your Contact Information]

---

Built with ❤️ using Flask, Wav2Vec 2.0, and DistilBERT AI Technologies
