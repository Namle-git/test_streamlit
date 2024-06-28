import streamlit as st
from flask import Flask, request, jsonify, send_file
import speech_recognition as sr
import base64
from io import BytesIO
from threading import Thread
import logging

# Initialize Streamlit app
st.title("Audio Recording Web App")

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
                        document.getElementById("status").innerText = "Recording uploaded";
                        document.getElementById("status").style.color = "green";
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
<p id="transcription">Transcription: </p>
"""

st.components.v1.html(html_code)

# Flask server setup
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    data = request.get_json()
    audio_base64 = data['audio'].split(',')[1]  # Remove the data URL scheme
    audio_data = base64.b64decode(audio_base64)
    
    # Save the audio data to a BytesIO object
    audio_file = BytesIO(audio_data)
    audio_file.seek(0)  # Reset file pointer to the beginning
    
    # Return success message
    return jsonify({'message': 'Audio uploaded successfully', 'audio': data['audio']})

@app.route('/get_audio', methods=['GET'])
def get_audio():
    audio_base64 = request.args.get('audio')
    audio_data = base64.b64decode(audio_base64.split(',')[1])
    audio_file = BytesIO(audio_data)
    audio_file.seek(0)  # Reset file pointer to the beginning
    
    return send_file(audio_file, mimetype='audio/wav', as_attachment=True, attachment_filename='recording.wav')

def run_flask():
    app.run(port=5000, debug=True, use_reloader=False)

# Start the Flask server in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()
