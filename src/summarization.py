import os
import json

from dotenv import load_dotenv
from google import genai


# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )


# Initialize Gemini client
client = genai.Client(
    api_key=API_KEY
)


def summarize_meeting(transcript):

    """
    Generate meeting summary, decisions,
    and action items using Gemini.
    """

    prompt = f"""
You are an AI meeting assistant.

Analyze the following meeting transcript.

Extract the following information:

1. A concise meeting summary.
2. Important discussion points.
3. Decisions made.
4. Action items.
5. Assigned person for each task.
6. Deadline for each task.

Important rules:

- Do not invent information.
- Only extract tasks explicitly discussed.
- Use null if the owner is not mentioned.
- Use null if the deadline is not mentioned.
- Separate decisions from action items.
- Return valid JSON only.
- Do not include markdown code blocks.

Use this exact JSON structure:

{{
    "meeting_summary": "string",
    "discussion_points": [],
    "decisions": [],
    "action_items": [
        {{
            "task": "string",
            "owner": "string or null",
            "deadline": "string or null",
            "status": "Pending"
        }}
    ]
}}

Meeting Transcript:

{transcript}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    result = response.text.strip()

    # Remove markdown code blocks if present
    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")

    # Convert response to Python dictionary
    data = json.loads(result.strip())

    return data