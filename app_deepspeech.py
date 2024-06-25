import streamlit as st
from streamlit_mic_recorder import speech_to_text

st.title("AI Assistant with Speech Recognition")

# Use streamlit-mic-recorder's built-in speech_to_text function
text = speech_to_text(
    language='en',
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=False,
    callback=None,
    args=(),
    kwargs={},
    key=None
)

# Display the transcription
if text:
    st.write(f"Transcription: {text}")
