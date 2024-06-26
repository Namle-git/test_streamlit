import streamlit as st
from streamlit_mic_recorder import mic_recorder
import streamlit.components.v1 as components

st.title("AI Assistant with Automatic Speech Recognition")

# Function to automatically record and transcribe audio
transcription = mic_recorder(
    start_prompt="Record",
    stop_prompt="Stop",
    just_once=True,
    use_container_width=True,
    callback=None,
    args=(),
    kwargs={},
    key="mic_recorder"
)
