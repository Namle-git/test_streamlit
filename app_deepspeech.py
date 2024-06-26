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
function logIframeDetails() {
    function findAndLogIframes() {
        let iframes = document.querySelectorAll('iframe');

        if (iframes.length > 0) {
            clearInterval(iframeInterval);

            console.log('Found iframes:', iframes);

            iframes.forEach(iframe => {
                console.log('Iframe title:', iframe.title);
                console.log('Iframe src:', iframe.src);
            });
        } else {
            console.log('No iframes found yet.');
        }

        let bodyElement = document.body;
        if (bodyElement) {
            console.log('Current body element structure:', bodyElement.innerHTML);
        } else {
            console.log('Body element not found.');
        }
    }

    let iframeInterval = setInterval(findAndLogIframes, 500);
}

document.addEventListener('DOMContentLoaded', logIframeDetails);
</script>
"""

# Embed the JavaScript code into the Streamlit app
components.html(js_code, height=0)

st.write("Check the console for iframe details.")
