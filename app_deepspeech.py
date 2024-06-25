import streamlit as st
from streamlit_mic_recorder import speech_to_text
import time

st.title("AI Assistant with Automatic Speech Recognition")

# Function to automatically record and transcribe audio
def automatic_recording_and_transcription(duration: int = 5):
    with st.spinner(f'Recording for {duration} seconds...'):
        time.sleep(duration)  # Simulate the recording duration
        
        # Use speech_to_text to record and transcribe audio
        text = speech_to_text(
            language='en',
            start_prompt="",
            stop_prompt="",
            just_once=True,
            use_container_width=True,
            callback=None,
            args=(),
            kwargs={},
            key="mic_recorder"
        )
        return text

# Start automatic recording and transcription
transcription = automatic_recording_and_transcription(duration=5)

# Display the transcription
if transcription:
    st.write(f"Transcription: {transcription}")
else:
    st.write("No transcription available.")
