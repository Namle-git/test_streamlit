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
        var iframes = document.getElementsByTagName('iframe');
        if (iframes.length === 0) {
          console.log("No iframes found.");
        } else {
          console.log("Found iframes:", iframes.length);
        }
        for (var i = 0; i < iframes.length; i++) {
          var iframe = iframes[i];
          console.log("Checking iframe", i, "with src:", iframe.src);
          var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
          if (iframeDocument) {
            var recordButton = iframeDocument.querySelector('button.myButton');
            if (recordButton) {
              console.log("Record button found in iframe", i, "clicking...");
              recordButton.click();
              return;
            } else {
              console.log("Record button not found in iframe", i);
            }
          } else {
            console.log("Iframe document not accessible for iframe", i);
          }
        }
        if (retries > 0) {
          console.log("Retrying... attempts left:", retries);
          setTimeout(function() { simulateButtonClick(retries - 1); }, 2000);
        } else {
          console.log("Retries exhausted. Record button not found.");
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
