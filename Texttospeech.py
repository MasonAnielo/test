import streamlit as st
import speech_recognition as sr
import tempfile

st.title("🎤 Lecture Transcriber (Light Version)")
st.write("Upload a `.wav` audio file to transcribe it to text.")

uploaded_file = st.file_uploader("Upload audio file", type=["wav"])

if uploaded_file is not None:
    recognizer = sr.Recognizer()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    with sr.AudioFile(tmp_path) as source:
        audio_data = recognizer.record(source)
        st.info("⏳ Transcribing...")
        try:
            text = recognizer.recognize_google(audio_data)
            st.subheader("📝 Transcription")
            st.write(text)

            # Highlighting logic
            keywords = ["important", "definition", "summary", "remember", "exam"]
            for word in keywords:
                text = text.replace(word, f"**:orange[{word.upper()}]**")
            st.subheader("✨ Highlighted")
            st.markdown(text)

        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError:
            st.error("❌ Speech Recognition service failed.")
