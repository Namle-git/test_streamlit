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
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/transcribe", true);
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
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/update_transcription", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ transcription: transcriptionText }));
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

# Endpoint to handle the audio upload and transcription
if st.query_params().get("transcribe"):
    import json
    data = json.loads(st.query_params().get("transcribe")[0])
    transcription = transcribe_audio(data['audio'])
    st.query_params(transcription=transcription)

# Endpoint to update transcription
if st.query_params().get("update_transcription"):
    import json
    data = json.loads(st.query_params().get("update_transcription")[0])
    st.write(f"Transcription: {data['transcription']}")
