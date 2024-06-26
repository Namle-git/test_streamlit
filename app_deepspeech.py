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

# Start automatic recording and transcription
transcription = automatic_recording_and_transcription(duration=5)

# JavaScript to interact with the button inside the iframe
st.markdown("""
<script>
document.addEventListener("DOMContentLoaded", function() {
    function tryClickButton(attempts) {
        var iframe = document.querySelector('iframe[src*="streamlit_mic_recorder"]');
        if (iframe && iframe.contentWindow) {
            try {
                var iframeDocument = iframe.contentWindow.document;
                var button = iframeDocument.querySelector('.myButton');

                if (button) {
                    button.click();
                    console.log('Button inside iframe clicked');
                } else if (attempts > 0) {
                    console.log('Button not found, retrying...');
                    setTimeout(function() {
                        tryClickButton(attempts - 1);
                    }, 1000); // Retry after 1 second
                } else {
                    console.log('Failed to click the button after 3 attempts');
                }
            } catch (e) {
                console.log('Error accessing iframe content:', e);
            }
        } else if (attempts > 0) {
            console.log('Iframe not loaded yet, retrying...');
            setTimeout(function() {
                tryClickButton(attempts - 1);
            }, 1000); // Retry after 1 second
        } else {
            console.log('Iframe not loaded after 3 attempts');
        }
    }

    // Wait for the iframe to load and then start trying to click the button
    var iframe = document.querySelector('iframe[src*="streamlit_mic_recorder"]');
    iframe.onload = function() {
        tryClickButton(3);
    };
});
</script>
""", unsafe_allow_html=True)

# Display the transcription
if transcription:
    st.write(f"Transcription: {transcription}")
else:
    st.write("No transcription available.")
