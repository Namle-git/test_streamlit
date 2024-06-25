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

# Add the HTML and JavaScript to simulate the button click with correct class name inside the iframe
components.html(
    """
    <script>
      function simulateButtonClick(retries) {
        console.log("Checking for iframe...");
        var iframe = document.querySelector('iframe[src*="streamlit_mic_recorder.streamlit_mic_recorder"]');
        if (iframe) {
          var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
          var recordButton = iframeDocument.querySelector('button.myButton');
          if (recordButton) {
            console.log("Record button found, clicking...");
            recordButton.click();
          } else {
            console.log("Record button not found in iframe.");
            if (retries > 0) {
              setTimeout(function() { simulateButtonClick(retries - 1); }, 2000);
            } else {
              console.log("Retries exhausted. Record button not found.");
            }
          }
        } else {
          console.log("Iframe not found.");
          if (retries > 0) {
            setTimeout(function() { simulateButtonClick(retries - 1); }, 2000);
          } else {
            console.log("Retries exhausted. Iframe not found.");
          }
        }
      }

      // Start the simulation with 10 retries
      setTimeout(function() { simulateButtonClick(10); }, 5000);
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
