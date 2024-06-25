import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np
import wave
import speech_recognition as sr
import os

st.title("AI Assistant with Speech Recognition")

# Define the audio processing callback function
def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    audio_data = frame.to_ndarray()
    audio_buffer = audio_data.tobytes()

    # Save audio buffer to a file for recognition
    with wave.open("temp_audio.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio_buffer)

    return frame

# Function to transcribe audio using Google Speech Recognition
def transcribe_audio(filename: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results; {e}"

# Define a function to handle the whole process
def record_and_transcribe():
    webrtc_ctx = webrtc_streamer(
        key="speech-recognition",
        mode=WebRtcMode.SENDRECV,
        client_settings=ClientSettings(
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"audio": True, "video": False},
        ),
        audio_frame_callback=audio_frame_callback,
        async_processing=True,
    )

    if webrtc_ctx.state.playing:
        st.write("Recording... please wait for 5 seconds.")
        st.session_state["recording"] = True

    if "recording" in st.session_state and not webrtc_ctx.state.playing:
        st.session_state["recording"] = False
        st.write("Recording stopped.")
        if os.path.exists("temp_audio.wav"):
            st.session_state["transcription"] = transcribe_audio("temp_audio.wav")
            os.remove("temp_audio.wav")

    if "transcription" in st.session_state:
        return st.session_state["transcription"]

# Call the function and display the result
transcription = record_and_transcribe()
if transcription:
    st.write(f"Transcription: {transcription}")
