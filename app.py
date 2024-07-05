import streamlit as st
import os

st.title("Audio Processing")

def get_audio_path():
    upload_folder = os.path.join(os.environ['HOME'], 'site', 'wwwroot', 'uploads')
    path_file = os.path.join(upload_folder, 'audio_path.txt')
    try:
        with open(path_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

audio_path = get_audio_path()

if audio_path:
    st.audio(audio_path)
    st.write(f"Audio file path: {audio_path}")
    # Add your audio processing logic here
else:
    st.write("No audio file uploaded yet.")
