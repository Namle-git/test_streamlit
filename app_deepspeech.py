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

st.write("loaded")

# Define your JavaScript code
js_code = """
<script>
// Function to parse HTML and interact with the iframe and button
function interactWithIframe() {
    // Function to find and interact with the iframe
    function findIframeAndClickButton() {
        // Find the iframe with the specific title
        let iframe = document.querySelector('iframe[title="streamlit_mic_recorder.streamlit_mic_recorder"]');

        if (iframe) {
            // Clear the interval once the iframe is found
            clearInterval(iframeInterval);
            
            // Wait for the iframe to load its content
            iframe.addEventListener('load', function() {
                // Get the iframe's content window and document
                let iframeDocument = iframe.contentDocument || iframe.contentWindow.document;

                // Find the button with the class 'myButton' within the iframe
                let button = iframeDocument.querySelector('.myButton');

                if (button) {
                    // Click the button
                    button.click();
                    console.log('Button clicked!');
                } else {
                    console.error('Button with class "myButton" not found in the iframe.');
                }
            });
        } else {
            console.error('Iframe with title "streamlit_mic_recorder.streamlit_mic_recorder" not found.');
        }
    }

    // Check for the iframe every 500ms until it is found
    let iframeInterval = setInterval(findIframeAndClickButton, 500);
}

// Wait for the DOM to be fully loaded before running the function
document.addEventListener('DOMContentLoaded', interactWithIframe);
</script>
"""

# Use st.write to include the JavaScript in an HTML component
st.components.v1.html(js_code, height=0)
