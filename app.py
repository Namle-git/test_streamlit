import streamlit as st
from flask import Flask, request, jsonify
import speech_recognition as sr
import base64
from io import BytesIO
from threading import Thread
import requests

# Initialize Streamlit app
st.title("Speech Recognition Web App")

# HTML and JavaScript for recording audio
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
                        const transcriptionEvent = new CustomEvent('transcriptionComplete', { detail: data.transcription });
                        document.dispatchEvent(transcriptionEvent);
                    });
                }
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

<p id="transcription">Transcription: </p>
"""

st.components.v1.html(html_code)

# JavaScript event listener to handle transcription result
transcription_code = """
<script>
document.addEventListener('transcriptionComplete', (event) => {
    const transcriptionText = event.detail;
    const transcriptionElement = document.getElementById("transcription");
    transcriptionElement.innerHTML = "Transcription: " + transcriptionText;

    // Send the transcription back to Streamlit
    fetch('/transcription', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ transcription: transcriptionText })
    });
});
</script>
"""

st.components.v1.html(transcription_code)

# Flask server setup
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    data = request.get_json()
    audio_base64 = data['audio'].split(',')[1]  # Remove the data URL scheme
    audio_data = base64.b64decode(audio_base64)
    
    recognizer = sr.Recognizer()
    audio_file = BytesIO(audio_data)
    
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        transcription = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        transcription = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        transcription = f"Could not request results from Google Speech Recognition service; {e}"
    
    return jsonify({'transcription': transcription})

@app.route('/transcription', methods=['POST'])
def transcription():
    data = request.get_json()
    transcription = data['transcription']
    st.write(f"Transcription: {transcription}")
    return '', 204  # No Content response

def run_flask():
    app.run(debug=True, port=5000, use_reloader=False)

# Start the Flask server in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()
