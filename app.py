import streamlit as st
import base64
from io import BytesIO
from pydub import AudioSegment
import streamlit.components.v1 as components
import time

st.title("Audio Recorder in Streamlit")

# Initialize session state for audio data
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = ""

# Initialize session state for audio data
if 'query_params' not in st.session_state:
    st.session_state.query_params = ""

# JavaScript for audio recording and setting session state
record_audio_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update URL Example</title>
</head>
<body>
    <h1>Update URL Example</h1>
    <button id="updateUrlButton">Add 'hello' to URL</button>

    <script>
        document.getElementById('updateUrlButton').addEventListener('click', function() {
            // Get the current URL
            let currentUrl = window.location.href;

            // Check if the URL already has query parameters
            if (currentUrl.indexOf('?') > -1) {
                // If yes, append the new parameter with &
                currentUrl += '&string=hello';
            } else {
                // If no, add the new parameter with ?
                currentUrl += '?string=hello';
            }

            // Update the URL by reloading the page with the new URL
            window.location.href = currentUrl;
        });
    </script>
</body>
</html>
"""

components.html(record_audio_html, height=200)

# Function to handle the custom event and update session state
def handle_audio_data():
    audio_data = st.session_state.audio_data
    if audio_data:
        audio_bytes = base64.b64decode(audio_data)
        audio = AudioSegment.from_file(BytesIO(audio_bytes), format="wav")
        st.audio(BytesIO(audio_bytes), format='audio/wav')
        st.write("Audio recorded successfully!")

if st.button("GET audio"):
    # Capture query parameters sent by the JavaScript
    query_params = st.query_params.to_dict()
    st.session_state.query_params=query_params
    st.write("This is the query_params")
    st.write(st.session_state.query_params)
    
    st.write("This is the audio_data")
    if "audio_data" in query_params:
        st.session_state.audio_data = query_params["audio_data"][0]
    
    # Display the Base64 string if available
    if st.session_state.audio_data:
        st.write("Base64 Audio Data:")
        st.write(st.session_state.audio_data)
