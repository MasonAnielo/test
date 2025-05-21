import streamlit as st
import whisper
import tempfile
import os

# Load Whisper model once
model = whisper.load_model("small")

# Streamlit app title and instructions
st.title("🎤 Lecture Transcriber & Highlighter")
st.write("Upload an audio file (MP3, WAV, M4A) to get transcription with highlights.")

# Upload file
uploaded_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # Save uploaded file to a temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_audio_path = tmp_file.name

    # Transcribe using Whisper
    st.info("⏳ Transcribing... please wait...")
    result = model.transcribe(temp_audio_path)
    transcript = result["text"]

    # Display original transcription
    st.subheader("📝 Transcription")
    st.write(transcript)

    # Highlight keywords
    keywords = ["important", "definition", "summary", "key point", "remember", "exam"]
    highlighted_text = transcript

    for word in keywords:
        highlighted_text = highlighted_text.replace(
            word, f"**:orange[{word.upper()}]**"
        )

    # Display highlighted version
    st.subheader("✨ Highlighted Text")
    st.markdown(highlighted_text)

    # Clean up
    os.remove(temp_audio_path)
