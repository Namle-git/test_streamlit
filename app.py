import streamlit as st
import sounddevice as sd
import numpy as np
import io
import scipy.io.wavfile as wavfile

def record_audio(duration, sample_rate):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    return recording

st.title("Audio Recorder and Player")

duration = st.slider("Recording duration (seconds)", 1, 10, 5)
sample_rate = 44100

if st.button("Record"):
    st.write("Recording...")
    audio_data = record_audio(duration, sample_rate)
    st.write("Recording complete!")
    
    # Convert the NumPy array to bytes
    byte_io = io.BytesIO()
    wavfile.write(byte_io, sample_rate, audio_data)
    
    # Display the audio
    st.audio(byte_io.getvalue(), format="audio/wav")

st.write("Note: Make sure you've allowed microphone access in your browser.")
