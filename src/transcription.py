from faster_whisper import WhisperModel


# Load Whisper model
model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(audio_file):

    """
    Convert meeting audio into text.
    """

    segments, info = model.transcribe(
        audio_file,
        beam_size=5
    )

    transcript = []

    for segment in segments:
        transcript.append(segment.text.strip())

    return " ".join(transcript)