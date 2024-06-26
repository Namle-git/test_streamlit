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

import streamlit as st

# Define your JavaScript code
js_code = """
<script>
// Function to log all iframe titles and src attributes
function logIframeDetails() {
    // Function to find and log iframe details
    function findAndLogIframes() {
        // Find all iframes on the page
        let iframes = document.querySelectorAll('iframe');

        if (iframes.length > 0) {
            // Clear the interval once iframes are found
            clearInterval(iframeInterval);

            console.log('Found iframes:', iframes);

            iframes.forEach(iframe => {
                console.log('Iframe title:', iframe.title);
                console.log('Iframe src:', iframe.src);
            });
        } else {
            console.log('No iframes found yet.');
        }
    }

    // Check for iframes every 500ms until they are found
    let iframeInterval = setInterval(findAndLogIframes, 500);
}

// Wait for the DOM to be fully loaded before running the function
document.addEventListener('DOMContentLoaded', logIframeDetails);
</script>
"""

# Use st.write to include the JavaScript in an HTML component
st.components.v1.html(js_code, height=0)

