import streamlit as st
from flask import Flask, request, jsonify, send_file
import base64
import os
from io import BytesIO
from threading import Thread
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Flask server setup
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_audio():
    logging.debug("Received audio upload request")
    data = request.get_json()
    audio_base64 = data['audio'].split(',')[1]  # Remove the data URL scheme
    audio_data = base64.b64decode(audio_base64)
    
    # Save the audio data to a file
    audio_id = 'recording.wav'
    audio_path = os.path.join(UPLOAD_FOLDER, audio_id)
    with open(audio_path, 'wb') as audio_file:
        audio_file.write(audio_data)
    
    logging.debug("Audio uploaded successfully")
    # Return the audio ID
    return jsonify({'message': 'Audio uploaded successfully', 'audio_id': audio_id})

@app.route('/get_audio/<audio_id>', methods=['GET'])
def get_audio(audio_id):
    logging.debug("Received get audio request")
    audio_path = os.path.join(UPLOAD_FOLDER, audio_id)
    if not os.path.exists(audio_path):
        return "Audio not found", 404

    logging.debug("Sending audio file")
    return send_file(audio_path, mimetype='audio/wav', as_attachment=True, attachment_filename=audio_id)

def run_flask():
    app.run(port=5000, debug=True, use_reloader=False)

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

                    fetch('/upload', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ audio: base64data })
                    }).then(response => {
                        return response.json();
                    }).then(data => {
                        // Send a message to the Streamlit app with the audio ID
                        const audioId = data.audio_id;
                        const audioIdMessage = new CustomEvent('audioIdMessage', { detail: { audioId } });
                        window.dispatchEvent(audioIdMessage);
                    });
                }

                document.getElementById("status").innerText = "Recording stopped";
                document.getElementById("status").style.color = "black";
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // Record for 5 seconds
        });
}

document.addEventListener('DOMContentLoaded', (event) => {
    startRecording();
});
</script>

<p id="status">Status: Not recording</p>
<div id="playback"></div>
"""

st.components.v1.html(html_code)

# JavaScript to communicate with Streamlit
st.write("""
<script>
window.addEventListener('audioIdMessage', function(event) {
    const audioId = event.detail.audioId;
    fetch(`/_stcore/fn/call`, {
        method: 'POST',
        body: JSON.stringify({ name: 'save_audio_id', kwargs: { audio_id: audioId } }),
        headers: { 'Content-Type': 'application/json' }
    });
});
</script>
""")

# Save audio ID to session state
def save_audio_id(audio_id):
    st.session_state.audio_id = audio_id

st.query_params.clear()  # Ensure the URL is clean without query params

# Display the stored audio file if available
if st.session_state.audio_id:
    audio_id = st.session_state.audio_id
    audio_url = f"http://localhost:5000/get_audio/{audio_id}"
    st.audio(audio_url)
    st.write("Audio is displayed")  # Debugging line to confirm audio display
else:
    st.write("No audio found in session state")
