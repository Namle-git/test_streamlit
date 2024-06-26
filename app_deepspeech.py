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
// Function to log all top-level elements and their children
function logTopLevelElements() {
    // Wait for the DOM to be fully loaded
    document.addEventListener('DOMContentLoaded', function() {
        // Get all top-level elements in the body
        let topElements = document.body.children;

        console.log('Top-level elements:', topElements);

        // Log details of each top-level element and its children
        Array.from(topElements).forEach(element => {
            console.log('Element:', element);
            console.log('Element HTML:', element.outerHTML);

            // Log children of each top-level element
            let children = element.children;
            console.log('Children of element:', children);

            Array.from(children).forEach(child => {
                console.log('Child element:', child);
                console.log('Child element HTML:', child.outerHTML);
            });
        });
    });
}

// Call the function
logTopLevelElements();
</script>
"""

# Use st.write to include the JavaScript in an HTML component
st.components.v1.html(js_code, height=0)
