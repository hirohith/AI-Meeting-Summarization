import sqlite3
import json

from pathlib import Path


# Database location
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "meetings.db"


# Connect to database
def get_connection():

    return sqlite3.connect(DB_PATH)


# Create database table
def initialize_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            transcript TEXT,

            summary TEXT,

            decisions TEXT,

            action_items TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()

    conn.close()


# Save meeting
def save_meeting(
    title,
    transcript,
    summary,
    decisions,
    action_items
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO meetings (
            title,
            transcript,
            summary,
            decisions,
            action_items
        )

        VALUES (?, ?, ?, ?, ?)
    """, (

        title,

        transcript,

        summary,

        json.dumps(decisions),

        json.dumps(action_items)

    ))

    meeting_id = cursor.lastrowid

    conn.commit()

    conn.close()

    return meeting_id


# Load meeting
def load_meeting(meeting_id):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM meetings WHERE id = ?",
        (meeting_id,)
    )

    meeting = cursor.fetchone()

    conn.close()

    if meeting:

        return dict(meeting)

    return None
def update_action_items(meeting_id, action_items):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE meetings SET action_items = ? WHERE id = ?",
        (json.dumps(action_items), meeting_id)
    )

    conn.commit()
    conn.close()

def load_latest_meeting():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM meetings ORDER BY id DESC LIMIT 1"
    )

    meeting = cursor.fetchone()
    conn.close()

    if meeting:
        meeting = dict(meeting)
        meeting["decisions"] = json.loads(
            meeting["decisions"] or "[]"
        )
        meeting["action_items"] = json.loads(
            meeting["action_items"] or "[]"
        )
        return meeting

    return None    
def load_all_meetings():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, summary, created_at
        FROM meetings
        ORDER BY id DESC
    """)

    meetings = cursor.fetchall()
    conn.close()

    return [dict(meeting) for meeting in meetings]

