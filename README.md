# 🎙️ AI-Based Meeting Summarization & Action Item Tracking System

An AI-powered meeting assistant that converts meeting recordings and text transcripts into structured summaries, decisions, and actionable tasks.

The application uses **faster-whisper** for audio transcription, **Google Gemini** for meeting analysis, **Streamlit** for the interactive interface, and **SQLite** for persistent meeting storage.

## ✨ Features

- 🎧 **Audio Transcription:** Transcribe meeting recordings using faster-whisper.
- 📝 **Transcript Input:** Paste or edit meeting transcripts manually.
- 🤖 **AI Meeting Summarization:** Generate concise meeting summaries using Gemini.
- 💡 **Discussion Points & Decisions:** Extract key discussion points and decisions.
- ✅ **Action Item Extraction:** Identify tasks, owners, deadlines, and statuses.
- 🔍 **Action Item Tracking:** Search, edit, and update action items.
- 💾 **Persistent Storage:** Store meetings and action-item updates in SQLite.
- 🕘 **Meeting History:** Browse and load previously saved meetings.
- 📊 **Report Export:** Download reports in CSV, JSON, and PDF formats.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| Audio Transcription | faster-whisper |
| AI Summarization | Google Gemini API |
| Data Processing | Pandas |
| Database | SQLite |
| PDF Generation | ReportLab |
| Environment Variables | python-dotenv |

## 🔄 Application Workflow

1. Upload a meeting recording or enter a transcript.
2. Transcribe audio using faster-whisper, if an audio file is provided.
3. Review or edit the transcript.
4. Send the transcript to Gemini for analysis.
5. Generate the meeting summary, decisions, and action items.
6. Edit and track action items through the application.
7. Save meeting data and changes in SQLite.
8. Browse previous meetings and export reports.

## 📁 Project Structure

```text
AI-Meeting-Summarization/
├── app.py
├── requirements.txt
├── .gitignore
├── src/
│   ├── database.py
│   ├── summarization.py
│   └── transcription.py
└── data/
    └── meetings.db
```

> The `data/` directory and SQLite database are created locally when the application runs. They are excluded from the GitHub repository.

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hirohith/AI-Meeting-Summarization.git
```

Navigate to the project directory:

```bash
cd AI-Meeting-Summarization
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your own Gemini API key.

**Important:** Keep your API key private. Do not upload the `.env` file to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📤 Report Export

The application supports downloading:

- **CSV:** Action-item data for spreadsheet analysis.
- **JSON:** Structured meeting analysis data.
- **PDF:** A readable meeting report containing the summary, decisions, and action items.

## ⚠️ Limitations

- Transcription accuracy may vary depending on audio quality, background noise, accents, and speaker overlap.
- Gemini may occasionally extract incorrect task owners, deadlines, or decisions. Review generated results before relying on them.
- AI summarization requires a valid Gemini API key and internet access.
- The application is a prototype and is not designed for production-scale deployment.
- Meeting data is stored in a local SQLite database.

## 🔮 Future Improvements

- Speaker identification and diarization.
- Improved task-owner and deadline validation.
- Meeting title and metadata customization.
- User authentication and access control.
- Cloud database integration.
- Deployment for multi-user access.

## 👨‍💻 Author

**Rohith Sheru**

- GitHub: [@hirohith](https://github.com/hirohith)
- Project Repository: [AI-Meeting-Summarization](https://github.com/hirohith/AI-Meeting-Summarization)

## 📄 License

This project is intended for educational and portfolio purposes.
