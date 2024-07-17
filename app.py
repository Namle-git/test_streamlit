import streamlit as st
import numpy as np
import io
import soundfile as sf
from scipy.io import wavfile
import base64

st.title("Audio Recorder and Player")

# Create a button to start recording
st.write("Click the button below and allow microphone access to start recording")
record_button = st.button("Record Audio")

# Use st.empty to create a placeholder for the audio player
audio_player = st.empty()

# JavaScript to handle audio recording
js_code = """
<script>
let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = () => {
                    const base64data = reader.result;
                    sendAudioToStreamlit(base64data);
                }
            });

            // Stop recording after 5 seconds
            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000);
        });
}

function sendAudioToStreamlit(base64data) {
    fetch("", {
        method: "POST",
        body: JSON.stringify({"audio_data": base64data}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => response.json())
    .then(data => {
        window.parent.postMessage({type: "streamlit:setComponentValue", value: data.audio_data}, "*")
    })
    .catch(error => console.error('Error:', error));
}

if (document.getElementById('record-button')) {
    document.getElementById('record-button').addEventListener('click', startRecording);
}
</script>
"""

# Inject JavaScript code
st.components.v1.html(js_code, height=0)

# Handle the received audio data
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None

if st.session_state.audio_data:
    # Remove the "data:audio/wav;base64," prefix
    audio_data = st.session_state.audio_data.split(",")[1]
    audio_bytes = base64.b64decode(audio_data)
    
    # Read the audio data
    with io.BytesIO(audio_bytes) as audio_io:
        data, samplerate = sf.read(audio_io)
    
    # Convert to 16-bit PCM
    audio_data_16bit = (data * 32767).astype(np.int16)
    
    # Create a BytesIO object for the WAV file
    wav_bytes = io.BytesIO()
    wavfile.write(wav_bytes, samplerate, audio_data_16bit)
    wav_bytes.seek(0)
    
    # Display the audio
    audio_player.audio(wav_bytes, format="audio/wav")

# Handle POST requests with audio data
if st.experimental_user.audio_data:
    st.session_state.audio_data = st.experimental_user.audio_data
    st.experimental_user.audio_data = None
    st.experimental_rerun()
