import streamlit as st
from threading import Thread

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

# HTML and JavaScript for recording audio with a button
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
                console.log("Data available event: ", event);
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

                    fetch('https://simonaireceptionistchatbot.azurewebsites.net/upload', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ audio: base64data })
                    }).then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    }).then(data => {
                        console.log("Received response:", data);
                        if (data.error) {
                            throw new Error(data.error);
                        }
                        const audioId = data.audio_id;
                        const audioIdMessage = new CustomEvent('audioIdMessage', { detail: { audioId } });
                        window.dispatchEvent(audioIdMessage);
                    }).catch(error => {
                        console.error("Error uploading audio:", error);
                        document.getElementById("status").innerText = "Error uploading audio";
                        document.getElementById("status").style.color = "red";
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
            document.getElementById("status").style.color = "red";
        });
}

document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM content loaded");
    document.getElementById("startButton").addEventListener("click", startRecording);
});
</script>

<button id="startButton">Start Recording</button>
<p id="status">Status: Not recording</p>
<div id="playback"></div>
"""

# Include the HTML and JavaScript in the Streamlit app
st.components.v1.html(html_code)

# JavaScript to communicate with Streamlit
st.write("""
<script>
window.addEventListener('audioIdMessage', function(event) {
    console.log("audioIdMessage event received:", event.detail.audioId);
    const audioId = event.detail.audioId;
    fetch('https://simonaireceptionistchatbot.azurewebsites.net/streamlit_set_audio_id', {
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
    audio_url = f"https://simonaireceptionistchatbot.azurewebsites.net/get_audio/{audio_id}"
    st.audio(audio_url)
    st.write("Audio is displayed")  # Debugging line to confirm audio display
else:
    st.write("No audio found in session state")
