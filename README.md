# 🤖 AI-Based Meeting Summarization & Action Item Tracking System

## 📌 Overview

The **AI-Based Meeting Summarization & Action Item Tracking System** is an AI-powered Streamlit web application that converts meeting recordings and text transcripts into structured meeting summaries.

The application uses **Whisper** for speech-to-text transcription and **Google Gemini AI** to identify important discussion points, key decisions, and actionable tasks.

It also provides meeting history, action item tracking, and report export functionality, helping users manage meeting information efficiently.

## ✨ Features

- 🎙️ **Audio Upload:** Upload meeting recordings in MP3, WAV, and M4A formats.
- 📝 **Speech-to-Text Transcription:** Convert audio recordings into text using OpenAI Whisper.
- ✍️ **Manual Transcript Input:** Enter or edit meeting transcripts manually.
- 🤖 **AI-Powered Summarization:** Generate structured meeting summaries using Google Gemini.
- 💬 **Discussion Points:** Automatically extract important discussion topics.
- ✅ **Decision Extraction:** Identify key decisions made during meetings.
- 📋 **Action Item Tracking:** Extract, search, and edit assigned tasks.
- 📚 **Meeting History:** Save and access previously processed meetings.
- 📊 **Report Export:** Export meeting reports in CSV, JSON, and PDF formats.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application interface |
| Whisper | Audio transcription |
| Google Gemini AI | AI-based summarization and information extraction |
| SQLite | Database management |
| Pandas | Data handling and processing |
| ReportLab | PDF report generation |

## 📂 Project Structure

```text
meeting-ai-assistant/
│
├── app.py
├── requirements.txt
├── README.md
│
└── src/
    ├── database.py
    ├── transcription.py
    └── summarization.py
```

## ⚙️ Installation and Setup

### 1. Install Python

Install Python 3.9 or a compatible version.

### 2. Clone the Repository

```bash
git clone https://github.com/hirohith/AI-Meeting-Summarization.git
```

Navigate to the project directory:

```bash
cd AI-Meeting-Summarization
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API Key

Create a `.env` file in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your valid API key.

> ⚠️ **Security Note:** Never upload your `.env` file or expose your API key on GitHub.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your default browser.

## 🚀 How to Use

1. Open the **Meeting Overview** page.
2. Select your preferred input method:
   - Audio Recording
   - Text Transcript
3. Upload an audio recording or enter a transcript manually.
4. If using audio, click **Transcribe Audio** to generate the transcript.
5. Review and edit the transcript if necessary.
6. Click **Generate Meeting Summary**.
7. View the generated:
   - Meeting Summary
   - Discussion Points
   - Key Decisions
   - Action Items
8. Navigate to **Action Items** to search and edit tasks.
9. Open **Meeting History** to access previously saved meetings.
10. Navigate to **Export Reports** to download meeting information in CSV, JSON, or PDF format.

## 🗄️ Database

The application uses **SQLite** to store meeting-related information.

The database maintains:

- Meeting transcripts
- Generated summaries
- Discussion points
- Key decisions
- Extracted action items

The database is initialized automatically when the application runs. A new database is created if no existing database file is found.

## 🔑 Requirements and Notes

- A valid Google Gemini API key is required for AI-based summarization.
- Audio transcription requires Whisper and may need additional system dependencies.
- Supported audio formats: MP3, WAV, and M4A.
- Internet connectivity is required for Gemini API access.
- The project is developed as a prototype and demonstration application.
- Avoid including confidential meeting recordings, API keys, or private information in the shared repository.

## 👨‍💻 Author

**Sheru Rohith**

- GitHub: [@hirohith](https://github.com/hirohith)
- LinkedIn: [Sheru Rohith](https://linkedin.com/in/sheru-rohith-535b5432b)

---

⭐ If you find this project useful, consider giving the repository a star!
