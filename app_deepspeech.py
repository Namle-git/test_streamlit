import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import numpy as np
from pydub import AudioSegment
import io

st.title("AI Assistant with Speech Recognition")

# Function to transcribe audio using Google Speech Recognition
def transcribe_audio(audio_data: bytes) -> str:
    recognizer = sr.Recognizer()
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
    
    with io.BytesIO() as wav_buffer:
        audio_segment.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        audio_file = sr.AudioFile(wav_buffer)
        with audio_file as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                return "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                return f"Could not request results; {e}"

# Use streamlit-mic-recorder to record audio
audio_data = audio = mic_recorder(
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=False,
    format="webm",
    callback=None,
    args=(),
    kwargs={},
    key=None
)

if audio_data:
    st.audio(audio_data, format="audio/wav")
    transcription = transcribe_audio(audio_data)
    st.write(f"Transcription: {transcription}")
