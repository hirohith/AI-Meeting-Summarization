import streamlit as st
import pandas as pd
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from src.database import (
    initialize_db,
    save_meeting,
    update_action_items,
    load_latest_meeting,
    load_all_meetings,
    load_meeting
)

from src.transcription import transcribe_audio
from src.summarization import summarize_meeting
from src.database import (
    initialize_db,
    save_meeting,
    update_action_items,
    load_latest_meeting
)
# Initialize SQLite database
initialize_db()
# Restore the latest saved meeting after a refresh
if "meeting_result" not in st.session_state:
    saved_meeting = load_latest_meeting()

    if saved_meeting:
        st.session_state["meeting_result"] = {
            "meeting_summary": saved_meeting.get("summary", ""),
            "discussion_points": [],
            "decisions": saved_meeting.get("decisions", []),
            "action_items": saved_meeting.get("action_items", [])
        }

        st.session_state["meeting_id"] = saved_meeting["id"]
        st.session_state["transcript"] = saved_meeting.get(
            "transcript", ""
        )
        st.session_state["action_items_data"] = saved_meeting.get(
            "action_items", []
        )


st.set_page_config(
    page_title="Meeting AI Assistant",
    page_icon="🎙️",
    layout="wide"
)


st.title("AI-Based Meeting Summarization")

st.subheader(
    "Meeting Summary & Action Item Tracking System"
)

st.write(
    "Convert meeting recordings and transcripts into "
    "structured summaries, decisions, and action items."
)


# ---------------- SIDEBAR ----------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a section",
    [
        "Meeting Overview",
        "Action Items",
        "Export Reports",
        "Meeting History"
    ]
)


# ---------------- MEETING OVERVIEW ----------------

if page == "Meeting Overview":

    st.header("Meeting Input")

    input_type = st.radio(
        "Choose meeting input type",
        ["Audio Recording", "Text Transcript"],
        horizontal=True
    )


    # AUDIO INPUT

    if input_type == "Audio Recording":

        st.subheader("Upload Meeting Recording")

        audio_file = st.file_uploader(
            "Upload your meeting audio",
            type=["mp3", "wav", "m4a"]
        )

        if audio_file is not None:

            st.audio(audio_file)

            if st.button("Transcribe Audio"):

                with st.spinner(
                    "Transcribing audio..."
                ):

                    try:

                        transcript = transcribe_audio(
                            audio_file
                        )

                        st.session_state["transcript"] = (
                            transcript
                        )

                        st.success(
                            "Transcription completed!"
                        )

                    except Exception as e:

                        st.error(
                            f"Transcription failed: {e}"
                        )


    # TEXT INPUT

    else:

        st.subheader("Enter Meeting Transcript")

        transcript = st.text_area(
            "Paste your meeting transcript here",
            height=300,
            placeholder="Enter the meeting conversation...",
            key="manual_transcript"
        )

        if transcript.strip():

            st.write(
                "Words:",
                len(transcript.split())
            )

            st.session_state["transcript"] = (
                transcript
            )


    # ---------------- TRANSCRIPT DISPLAY ----------------

    if "transcript" in st.session_state:

        st.divider()

        st.subheader("Meeting Transcript")

        edited_transcript = st.text_area(
            "Review or edit the transcript",
            value=st.session_state["transcript"],
            height=250,
            key="editable_transcript"
        )

        st.session_state["transcript"] = (
            edited_transcript
        )


        # ---------------- GEMINI PROCESSING ----------------

        if st.button("Generate Meeting Summary"):

            if edited_transcript.strip():

                with st.spinner(
                    "Gemini is analyzing the meeting..."
                ):

                    try:

                        result = summarize_meeting(
                            edited_transcript
                        )

                        st.session_state["meeting_result"] = result

                        # Save meeting to SQLite
                        meeting_id = save_meeting(
                            title="Meeting",
                            transcript=edited_transcript,
                            summary=result.get("meeting_summary", ""),
                            decisions=result.get("decisions", []),
                            action_items=result.get("action_items", [])
                        )

                        st.session_state["meeting_id"] = meeting_id

                        st.success(
                            f"Meeting analysis completed! Meeting ID: {meeting_id}"
                        )

                    except Exception as e:

                        st.error(
                            f"AI processing failed: {e}"
                        )

            else:

                st.warning(
                    "Please provide a meeting transcript."
                )


    # ---------------- DISPLAY RESULTS ----------------

    if "meeting_result" in st.session_state:

        result = st.session_state["meeting_result"]

        st.divider()

        st.header("Meeting Summary")

        st.write(
            result.get(
                "meeting_summary",
                "No summary available."
            )
        )


        # DISCUSSION POINTS

        st.subheader("Discussion Points")

        discussion_points = result.get(
            "discussion_points",
            []
        )

        for point in discussion_points:

            st.markdown(
                f"- {point}"
            )


        # DECISIONS

        st.subheader("Decisions")

        decisions = result.get(
            "decisions",
            []
        )

        for decision in decisions:

            st.markdown(
                f"- {decision}"
            )


        # ACTION ITEMS

        st.subheader("Action Items")

        action_items = result.get(
            "action_items",
            []
        )

        if action_items:

            df = pd.DataFrame(
                action_items
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info(
                "No action items were identified."
            )


# ---------------- ACTION ITEMS ----------------

elif page == "Action Items":

    st.header("Action Item Tracking")

    if "meeting_result" not in st.session_state:

        st.info("Generate a meeting summary first.")

    else:

        # Initialize action items
        if "action_items_data" not in st.session_state:

            st.session_state["action_items_data"] = (
                st.session_state["meeting_result"].get(
                    "action_items", []
                )
            )

        # Save changes from the editor
        def save_action_items():

            edited_data = st.session_state[
                "action_items_editor"
            ]

            original_df = pd.DataFrame(
                st.session_state["action_items_data"]
            )

            # Update edited cells
            for row_index, changes in edited_data.get(
                "edited_rows", {}
            ).items():

                for column, value in changes.items():

                    original_df.loc[
                        row_index, column
                    ] = value

            # Add new rows
            for new_row in edited_data.get(
                "added_rows", []
            ):

                original_df = pd.concat(
                    [
                        original_df,
                        pd.DataFrame([new_row])
                    ],
                    ignore_index=True
                )

            # Delete rows
            deleted_rows = sorted(
                edited_data.get(
                    "deleted_rows", []
                ),
                reverse=True
            )

            for row_index in deleted_rows:

                if row_index < len(original_df):

                    original_df = original_df.drop(
                        original_df.index[row_index]
                    )

            original_df = original_df.reset_index(
                drop=True
            )

            updated_items = original_df.to_dict(
                orient="records"
            )

            st.session_state[
                "action_items_data"
            ] = updated_items

            meeting_id = st.session_state.get("meeting_id")

            if meeting_id:
                update_action_items(meeting_id, updated_items)


        # Search input
        st.subheader("Search Action Items")

        search_query = st.text_input(
            "Search by task, owner, deadline, or status",
            placeholder="Example: Rahul, Friday, Pending..."
        )

        # Create DataFrame
        df = pd.DataFrame(
            st.session_state["action_items_data"]
        )

        # Filter data
        if search_query.strip():

            search_query = search_query.lower()

            mask = df.astype(str).apply(
                lambda row: row.str.lower().str.contains(
                    search_query,
                    na=False
                ).any(),
                axis=1
            )

            filtered_df = df[mask]

        else:

            filtered_df = df

        st.write(
            f"Showing {len(filtered_df)} of {len(df)} action items"
        )

        # Editable table
        st.subheader("Edit Action Items")

        st.data_editor(
            filtered_df,
            num_rows="dynamic",
            use_container_width=True,
            key="action_items_editor",
            on_change=save_action_items
        )

        st.success(
            "Action items are synchronized automatically."
        )




# ---------------- EXPORT REPORTS ----------------

elif page == "Export Reports":

    st.header("Export Meeting Reports")

    if "meeting_result" not in st.session_state:
        st.info("Generate a meeting summary first.")

    else:
        result = st.session_state["meeting_result"]

        st.subheader("Export Action Items as CSV")

        action_items = st.session_state.get(
            "action_items_data",
            result.get("action_items", [])
        )

        if action_items:
            df = pd.DataFrame(action_items)

            csv_data = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Action Items CSV",
                data=csv_data,
                file_name="meeting_action_items.csv",
                mime="text/csv"
            )
        else:
            st.divider()

        st.subheader("Export Complete Meeting as JSON")

        json_data = {
            "meeting_id": st.session_state.get("meeting_id"),
            "meeting_summary": result.get("meeting_summary", ""),
            "discussion_points": result.get("discussion_points", []),
            "decisions": result.get("decisions", []),
            "action_items": action_items
        }

        json_string = json.dumps(
            json_data,
            indent=4,
            ensure_ascii=False
        )

        st.download_button(
            label="Download Meeting JSON",
            data=json_string,
            file_name="meeting_report.json",
            mime="application/json"
        )

        st.divider()

        st.subheader("Export Meeting Report as PDF")

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter
        )

        styles = getSampleStyleSheet()
        story = []

        story.append(
            Paragraph("Meeting Summary Report", styles["Title"])
        )
        story.append(Spacer(1, 12))

        story.append(
            Paragraph("Meeting Summary", styles["Heading2"])
        )
        story.append(
            Paragraph(
                result.get("meeting_summary", "No summary available."),
                styles["BodyText"]
            )
        )
        story.append(Spacer(1, 12))

        story.append(
            Paragraph("Discussion Points", styles["Heading2"])
        )

        for point in result.get("discussion_points", []):
            story.append(
                Paragraph(f"- {point}", styles["BodyText"])
            )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph("Decisions", styles["Heading2"])
        )

        for decision in result.get("decisions", []):
            story.append(
                Paragraph(f"- {decision}", styles["BodyText"])
            )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph("Action Items", styles["Heading2"])
        )

        table_data = [
            ["Task", "Owner", "Deadline", "Status"]
        ]

        for item in action_items:
            table_data.append([
                str(item.get("task", "")),
                str(item.get("owner", "")),
                str(item.get("deadline", "")),
                str(item.get("status", ""))
            ])

        action_table = Table(
            table_data,
            repeatRows=1
        )

        action_table.setStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])

        story.append(action_table)

        doc.build(story)

        pdf_buffer.seek(0)

        st.download_button(
            label="Download Meeting PDF",
            data=pdf_buffer.getvalue(),
            file_name="meeting_report.pdf",
            mime="application/pdf"
        )
# ---------------- MEETING HISTORY ----------------

# ---------------- MEETING HISTORY ----------------

elif page == "Meeting History":

    st.header("Meeting History")

    meetings = load_all_meetings()

    if not meetings:
        st.info("No saved meetings found.")

    else:
        history_df = pd.DataFrame(meetings)

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("View a Saved Meeting")

        meeting_ids = [
            meeting["id"] for meeting in meetings
        ]

        selected_id = st.selectbox(
            "Select Meeting ID",
            meeting_ids
        )

        if st.button("Load Meeting"):
            selected_meeting = load_meeting(selected_id)

            if selected_meeting:
                st.session_state["meeting_result"] = {
                    "meeting_summary": selected_meeting.get(
                        "summary", ""
                    ),
                    "discussion_points": [],
                    "decisions": json.loads(
                        selected_meeting.get("decisions") or "[]"
                    ),
                    "action_items": json.loads(
                        selected_meeting.get("action_items") or "[]"
                    )
                }

                st.session_state["meeting_id"] = selected_meeting["id"]
                st.session_state["transcript"] = selected_meeting.get(
                    "transcript", ""
                )
                st.session_state["action_items_data"] = (
                    st.session_state["meeting_result"]["action_items"]
                )

                st.success(
                    f"Meeting {selected_id} loaded successfully!"
                )

                st.rerun()
            