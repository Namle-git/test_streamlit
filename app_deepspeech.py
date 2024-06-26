import streamlit as st
import requests

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
                        document.getElementById("transcription").innerHTML = "Transcription: " + data.transcription;
                    });
                }
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // Record for 5 seconds
        });
}
</script>

<button onclick="startRecording()">Start Recording</button>
<p id="transcription">Transcription: </p>
"""

st.components.v1.html(html_code)
