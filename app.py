import streamlit as st
from threading import Thread
from backend import run_flask  # Import the Flask app setup
import requests

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
var mediaRecorder;
var audioChunks = [];

function startRecording() {
    document.getElementById("status").innerText = "Recording...";
    document.getElementById("status").style.color = "red";

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                var audioBlob = new Blob(audioChunks);
                var fileReader = new FileReader();
                fileReader.readAsDataURL(audioBlob);
                fileReader.onloadend = function() {
                    var base64data = fileReader.result;

                    fetch('http://localhost:5000/upload', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ audio: base64data })
                    }).then(response => {
                        return response.json();
                    }).then(data => {
                        console.log("Received response:", data);  // Debug log
                        // Send a message to the Streamlit app with the audio ID
                        const audioId = data.audio_id;
                        const audioIdMessage = new CustomEvent('audioIdMessage', { detail: { audioId } });
                        window.dispatchEvent(audioIdMessage);
                    }).catch(error => {
                        console.error("Error uploading audio:", error);  // Error handling
                    });
                }

                document.getElementById("status").innerText = "Recording stopped";
                document.getElementById("status").style.color = "black";
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // Record for 5 seconds
        }).catch(error => {
            console.error("Error accessing microphone:", error);  // Error handling
            document.getElementById("status").innerText = "Error accessing microphone";
        });
}

document.addEventListener('DOMContentLoaded', (event) => {
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
        console.log("Streamlit session state updated:", data);  // Debug log
    }).catch(error => {
        console.error("Error updating Streamlit session state:", error);  // Error handling
    });
});
</script>
""", unsafe_allow_html=True)

# Flask endpoint to update session state
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/streamlit_set_audio_id', methods=['POST'])
def streamlit_set_audio_id():
    data = request.json
    audio_id = data['audio_id']
    st.session_state.audio_id = audio_id
    return jsonify({'message': 'Audio ID set in session state'})

def run_flask():
    app.run(port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Display the stored audio file if available
    if st.session_state.audio_id:
        audio_id = st.session_state.audio_id
        audio_url = f"http://localhost:5000/get_audio/{audio_id}"
        st.audio(audio_url)
        st.write("Audio is displayed")  # Debugging line to confirm audio display
    else:
        st.write("No audio found in session state")
