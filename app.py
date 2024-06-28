import streamlit as st
import speech_recognition as sr
import base64
from io import BytesIO
import json

# Initialize Streamlit app
st.title("Speech Recognition Web App")

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
                    const xhr = new XMLHttpRequest();
                    xhr.open("POST", "/upload_audio", true);
                    xhr.setRequestHeader("Content-Type", "application/json");
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            var json = JSON.parse(xhr.responseText);
                            const transcriptionEvent = new CustomEvent('transcriptionComplete', { detail: json.transcription });
                            document.dispatchEvent(transcriptionEvent);
                        }
                    };
                    xhr.send(JSON.stringify({ audio: base64data }));
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
});
</script>
"""

st.components.v1.html(transcription_code)

# Function to handle transcription in Streamlit
def transcribe_audio(audio_base64):
    audio_data = base64.b64decode(audio_base64.split(',')[1])  # Remove the data URL scheme
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

# Handle the audio upload and transcription
if 'audio_data' in st.session_state:
    transcription = transcribe_audio(st.session_state['audio_data'])
    st.write(f"Transcription: {transcription}")

# Function to update the session state with the uploaded audio
def update_audio_data():
    query_params = st.experimental_get_query_params()
    if 'audio_data' in query_params:
        st.session_state['audio_data'] = query_params['audio_data'][0]
        st.experimental_set_query_params(audio_data=None)

update_audio_data()

# Add a placeholder to update with the recorded audio data
if st.button('Record Audio'):
    st.experimental_set_query_params(audio_data="")  # This should trigger the JavaScript to start recording
