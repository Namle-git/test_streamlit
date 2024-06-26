import streamlit as st
import requests

st.title("Speech Recognition Web App")

# JavaScript for recording audio with an indicator and automatic timeout
html_code = """
<script>
var mediaRecorder;
var audioChunks = [];

function startRecording() {
    var indicator = document.getElementById("indicator");
    indicator.innerHTML = "Recording...";
    indicator.style.color = "red";

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
                        indicator.innerHTML = "Transcription: " + data.transcription;
                        indicator.style.color = "black";
                    });
                }
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // Record for 5 seconds
        });
}

window.onload = function() {
    startRecording();
}
</script>

<div id="indicator">Waiting to start recording...</div>
"""

st.components.v1.html(html_code)
