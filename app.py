import streamlit as st
import speech_recognition as sr
import base64
from io import BytesIO

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
                    document.querySelector('body').dispatchEvent(new CustomEvent('audioBlobReady', { detail: base64data }));
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

document.querySelector('body').addEventListener('audioBlobReady', (event) => {
    const base64data = event.detail;
    fetch('/transcription', {
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
});
</script>

<p id="status">Status: Not recording</p>
<div id="playback"></div>
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

def transcribe_audio(audio_base64):
    audio_data = base64.b64decode(audio_base64.split(',')[1])
    
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
    
    return transcription

# Handle transcription requests directly in Streamlit
if 'audio' in st.session_state:
    audio_base64 = st.session_state['audio']
    transcription = transcribe_audio(audio_base64)
    st.session_state['transcription'] = transcription
    st.write(f"Transcription: {transcription}")

# Display transcription result if available
if 'transcription' in st.session_state:
    st.write(f"Transcription: {st.session_state['transcription']}")

# JavaScript to fetch the transcription result
transcription_fetch_code = """
<script>
document.querySelector('body').addEventListener('transcriptionComplete', (event) => {
    const transcriptionText = event.detail;
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

st.components.v1.html(transcription_fetch_code)

# Endpoint to handle transcription post requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/transcription', methods=['POST'])
def handle_transcription():
    data = request.get_json()
    if 'audio' in data:
        st.session_state['audio'] = data['audio']
    if 'transcription' in data:
        st.session_state['transcription'] = data['transcription']
    return jsonify(success=True)

# Start the Flask server
from threading import Thread

def run_flask():
    app.run(port=8501)

flask_thread = Thread(target=run_flask)
flask_thread.start()
