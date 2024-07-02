import streamlit as st
from threading import Thread
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Streamlit app
st.title("Basic Audio Recording Web App")

# Initialize session state for audio
if "audio_data" not in st.session_state:
    st.session_state["audio_data"] = None

# HTML and JavaScript for recording audio with a button
html_code = """
<script>
var mediaRecorder;
var audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                var audioBlob = new Blob(audioChunks);
                var reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = function() {
                    var base64data = reader.result.split(',')[1];
                    fetch('/audio_upload', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ audio: base64data })
                    }).then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok: ' + response.statusText);
                        }
                        return response.json();
                    }).then(data => {
                        console.log("Received response:", data);
                    }).catch(error => {
                        console.error("Error uploading audio:", error);
                    });
                }
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // Record for 5 seconds
        }).catch(error => {
            console.error("Error accessing microphone:", error);
        });
}
</script>

<button onclick="startRecording()">Start Recording</button>
<p id="status">Status: Not recording</p>
"""

# Include the HTML and JavaScript in the Streamlit app
st.components.v1.html(html_code, height=200)

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/audio_upload', methods=['POST'])
def audio_upload_handler():
    try:
        data = request.json
        audio_data = base64.b64decode(data['audio'])
        st.session_state["audio_data"] = audio_data
        return jsonify({"message": "Audio received"}), 200
    except Exception as e:
        logging.error(f"Error uploading audio: {e}")
        return jsonify({"message": "Error uploading audio", "error": str(e)}), 500

# Function to run Flask server
def run_flask():
    app.run(host='0.0.0.0', port=8501, debug=True)

# Start Flask server in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Display the recorded audio if available
if st.session_state["audio_data"]:
    st.audio(st.session_state["audio_data"], format="audio/wav")
