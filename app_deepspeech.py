import streamlit as st
from streamlit_mic_recorder import speech_to_text
import time

st.title("AI Assistant with Automatic Speech Recognition")

# Function to automatically record and transcribe audio
def automatic_recording_and_transcription(duration: int = 5):
        text = speech_to_text(
            language='en',
            start_prompt="Record",
            stop_prompt="Stop",
            just_once=True,
            use_container_width=True,
            callback=None,
            args=(),
            kwargs={},
            key="mic_recorder"
        )
        return text

Here's how to integrate the JavaScript code into your Streamlit app to simulate the button click for the streamlit-mic-recorder component:

Complete Code
python
Copy code
import streamlit as st
from streamlit_mic_recorder import speech_to_text
import time
import streamlit.components.v1 as components

st.title("AI Assistant with Automatic Speech Recognition")

# Function to automatically record and transcribe audio
def automatic_recording_and_transcription(duration: int = 5):
    text = speech_to_text(
        language='en',
        start_prompt="Record",
        stop_prompt="Stop",
        just_once=True,
        use_container_width=True,
        callback=None,
        args=(),
        kwargs={},
        key="mic_recorder"
    )
    return text

# Add the HTML and JavaScript to simulate the button click
components.html(
    """
    <script>
      function simulateButtonClick() {
        var recordButton = document.querySelector('.myButton');
        if (recordButton) {
          recordButton.click();
        }
      }

      // Simulate the button click after 5 seconds
      setTimeout(simulateButtonClick, 5000);
    </script>
    """,
    height=0,  # Adjust height if needed
)

# Start automatic recording and transcription
transcription = automatic_recording_and_transcription(duration=5)

# Display the transcription
if transcription:
    st.write(f"Transcription: {transcription}")
else:
    st.write("No transcription available.")
