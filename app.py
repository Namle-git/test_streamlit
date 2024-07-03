import streamlit as st
import requests
import base64
from io import BytesIO
from pydub import AudioSegment

st.title("Audio Recorder in Streamlit")

# HTML and JavaScript code to record audio
record_audio_html = """
<script>
let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.start();
        });
}

function stopRecording() {
    mediaRecorder.stop();
    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
            const base64String = reader.result.split(',')[1];
            fetch('/upload_audio', {
                method: 'POST',
                body: JSON.stringify({ audio: base64String }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json())
              .then(data => {
                  document.getElementById("audio_url").value = data.audio_url;
              });
        };
    };
}
</script>
<button onclick="startRecording()">Start Recording</button>
<button onclick="stopRecording()">Stop Recording</button>
<input type="hidden" id="audio_url" name="audio_url">
"""

st.components.v1.html(record_audio_html)

audio_url = st.text_input("Recorded Audio URL", key="audio_url")

if audio_url:
    st.audio(audio_url, format='audio/wav')
