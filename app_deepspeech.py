import streamlit as st
from streamlit_mic_recorder import speech_to_text
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

# Add the HTML and JavaScript to simulate the button click with logging
components.html(
    """
    <script>
      function simulateButtonClick() {
        var recordButton = document.querySelector('.myButton');
        if (recordButton) {
          console.log("Button found, clicking...");
          recordButton.click();
        } else {
          console.log("Button not found, retrying...");
          setTimeout(simulateButtonClick, 1000);
        }
      }

      // Simulate the button click after a delay
      setTimeout(simulateButtonClick, 2000);
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
