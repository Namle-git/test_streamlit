import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
import io
import time

st.title("AI Assistant with Automatic Speech Recognition")

# Function to transcribe audio using Google Speech Recognition
def transcribe_audio(audio_data: bytes) -> str:
    recognizer = sr.Recognizer()
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")  # Adjust format if necessary

    with io.BytesIO() as wav_buffer:
        audio_segment.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        audio_file = sr.AudioFile(wav_buffer)
        with audio_file as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                return "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                return f"Could not request results; {e}"

# Automatically start and stop recording
def automatic_recording(duration: int = 5):
    with st.spinner(f'Recording for {duration} seconds...'):
        audio_data = mic_recorder(
            start_prompt="",
            stop_prompt="",
            just_once=True,
            use_container_width=False,
            format="webm",
            callback=None,
            args=(),
            kwargs={},
            key=None
        )
        time.sleep(duration)
        return audio_data

# Start automatic recording
audio_data = automatic_recording(duration=5)

if audio_data:
    audio_bytes = audio_data["audio_data"]
    st.audio(audio_bytes, format="audio/wav")  # Ensure the audio format is correct
    transcription = transcribe_audio(audio_bytes)
    st.write(f"Transcription: {transcription}")
else:
    st.write("No audio recorded.")
