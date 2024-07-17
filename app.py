import streamlit as st
import numpy as np
import io
import soundfile as sf
from scipy.io import wavfile

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
    fetch("http://localhost:8501/", {
        method: "POST",
        body: JSON.stringify({"audio_data": base64data}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => console.log(response))
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
if st.session_state.get('audio_data'):
    audio_data = st.session_state['audio_data']
    audio_bytes = io.BytesIO(audio_data)
    
    # Read the audio data
    data, samplerate = sf.read(audio_bytes)
    
    # Convert to 16-bit PCM
    audio_data_16bit = (data * 32767).astype(np.int16)
    
    # Create a BytesIO object for the WAV file
    wav_bytes = io.BytesIO()
    wavfile.write(wav_bytes, samplerate, audio_data_16bit)
    
    # Display the audio
    audio_player.audio(wav_bytes.getvalue(), format="audio/wav")

# Handle POST requests with audio data
if 'audio_data' in st.experimental_get_query_params():
    audio_data = st.experimental_get_query_params()['audio_data'][0]
    audio_bytes = io.BytesIO(audio_data.encode('utf-8'))
    st.session_state['audio_data'] = audio_bytes.getvalue()
    st.experimental_rerun()
