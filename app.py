import streamlit as st
from threading import Thread
import requests

# Function to run Flask server
def run_flask():
    import backend  # Import the backend module to ensure it runs
    backend.run_flask()

# Start the Flask server in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Initialize Streamlit app
st.title("Audio Recording Web App")

# Initialize session state for audio
if "audio_id" not in st.session_state:
    st.session_state["audio_id"] = None

# HTML and JavaScript for recording audio
html_code = """
<script>
console.log("Script loaded");

var mediaRecorder;
var audioChunks = [];

function startRecording() {
    console.log("Starting recording...");
    document.getElementById("status").innerText = "Recording...";
    document.getElementById("status").style.color = "red";

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            console.log("Microphone access granted");
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            console.log("MediaRecorder started");

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                console.log("Recording stopped");
                var audioBlob = new Blob(audioChunks);
                var fileReader = new FileReader();
                fileReader.readAsDataURL(audioBlob);
                fileReader.onloadend = function() {
                    var base64data = fileReader.result;
                    console.log("Audio data read as base64");

                    fetch('http://localhost:5000/upload', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ audio: base64data })
                    }).then(response => {
                        return response.json();
                    }).then(data => {
                        console.log("Received response:", data);
                        // Send a message to the Streamlit app with the audio ID
                        const audioId = data.audio_id;
                        const audioIdMessage = new CustomEvent('audioIdMessage', { detail: { audioId } });
                        window.dispatchEvent(audioIdMessage);
                    }).catch(error => {
                        console.error("Error uploading audio:", error);
                    });
                }

                document.getElementById("status").innerText = "Recording stopped";
                document.getElementById("status").style.color = "black";
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // Record for 5 seconds
        }).catch(error => {
            console.error("Error accessing microphone:", error);
            document.getElementById("status").innerText = "Error accessing microphone";
        });
}

document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM content loaded");
    startRecording();
});
</script>

<p id="status">Status: Not recording</p>
<div id="playback"></div>
"""

# Include the HTML and JavaScript in the Streamlit app
st.markdown(html_code, unsafe_allow_html=True)

# JavaScript to communicate with Streamlit
st.markdown("""
<script>
window.addEventListener('audioIdMessage', function(event) {
    const audioId = event.detail.audioId;
    fetch('http://localhost:5000/streamlit_set_audio_id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ audio_id: audioId })
    }).then(response => {
        return response.json();
    }).then(data => {
        console.log("Streamlit session state updated:", data);
    }).catch(error => {
        console.error("Error updating Streamlit session state:", error);
    });
});
</script>
""", unsafe_allow_html=True)

# Display the stored audio file if available
if st.session_state.audio_id:
    audio_id = st.session_state.audio_id
    audio_url = f"http://localhost:5000/get_audio/{audio_id}"
    st.audio(audio_url)
    st.write("Audio is displayed")  # Debugging line to confirm audio display
else:
    st.write("No audio found in session state")
