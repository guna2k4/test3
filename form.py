import streamlit as st
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import assemblyai as aai
from translate import Translator

# Global configuration
ASSEMBLY_AI_API_KEY = "6fcc70ef9823441d97116e3f8c5c5601"  # Replace with your actual AssemblyAI key

# Supported languages
SUPPORTED_LANGUAGES = {
    "Tamil": "ta",
    "Spanish": "es",
    "Turkish": "tr",
    "Japanese": "ja",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "English": "en"
}

# Define functions for audio processing
def audio_transcription(audio_file):
    aai.settings.api_key = ASSEMBLY_AI_API_KEY
    transcriber = aai.Transcriber()
    transcription = transcriber.transcribe(audio_file)
    return transcription

def text_translation(text, target_lang_code):
    translator = Translator(from_lang="en", to_lang=target_lang_code)
    return translator.translate(text)

# Function to record audio
def record_audio(duration):
    st.write("Recording...")
    recording = sd.rec(int(duration * 44100), samplerate=44100, channels=2, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    st.write("Recording finished.")
    return recording

# Layout
st.set_page_config(page_title="Voice-to-Text and Translation", layout="wide")

# Sidebar for user selection
user = st.sidebar.selectbox("Select User", ["User 1", "User 2"])

# Placeholder for the conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to handle conversation
def add_to_conversation(user, text, translation):
    st.session_state.conversation.append({
        "user": user,
        "text": text,
        "translation": translation
    })

# User 1 or User 2 interaction
if user == "User 1":
    st.title("User 1: Send Voice Message")
else:
    st.title("User 2: Send Voice Message")

# Record audio
duration = st.slider("Select duration (seconds)", 1, 10, 5)
if st.button("Record"):
    audio_data = record_audio(duration)
    wav_file = "recorded_audio.wav"
    write(wav_file, 44100, audio_data)
    st.success("Audio recorded and saved.")

    # Transcribe audio
    transcription_response = audio_transcription(wav_file)
    if transcription_response.status == aai.TranscriptStatus.error:
        st.error("Transcription Error")
    else:
        text = transcription_response.text
        st.success("Transcription successful!")

        # Select language for translation
        selected_language = st.selectbox("Select Language for Translation", list(SUPPORTED_LANGUAGES.keys()))
        lang_code = SUPPORTED_LANGUAGES[selected_language]
        translation = text_translation(text, lang_code)

        # Add to conversation
        add_to_conversation(user, text, translation)

# Display the conversation
st.header("Conversation")
for message in st.session_state.conversation:
    if message["user"] == "User 1":
        st.markdown(f"**User 1:** {message['text']}")
    else:
        st.markdown(f"**User 2:** {message['text']}")
    st.markdown(f"**Translation:** {message['translation']}")
