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

# Server-side processing of the transcription
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/transcription', methods=['POST'])
def transcription():
    data = request.get_json()
    transcription = data['transcription']
    st.write(f"Transcription: {transcription}")
    return '', 204  # No Content response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
