import streamlit as st
import requests
import base64

st.title("Audio Recorder and Player")

# Placeholder for audio player
audio_player = st.empty()

# Create buttons
col1, col2 = st.columns(2)
start_stop_button = col1.button("Start Recording", key="start_stop")
upload_button = col2.button("Upload Recording", key="upload", disabled=True)

# JavaScript to handle audio recording
js_code = """
<script>
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

function toggleRecording() {
    if (!isRecording) {
        startRecording();
    } else {
        stopRecording();
    }
}

function startRecording() {
    audioChunks = [];
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            isRecording = true;

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            // Update button text
            const button = window.parent.document.querySelector('button[kind="secondary"]:nth-of-type(1)');
            if (button) button.innerText = "Stop Recording";

            // Enable upload button
            const uploadButton = window.parent.document.querySelector('button[kind="secondary"]:nth-of-type(2)');
            if (uploadButton) uploadButton.disabled = false;
        });
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        isRecording = false;

        mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = () => {
                const base64data = reader.result;
                fetch('http://localhost:5000/save_audio', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ audio: base64data }),
                })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch((error) => console.error('Error:', error));
            }
        });

        // Update button text
        const button = window.parent.document.querySelector('button[kind="secondary"]:nth-of-type(1)');
        if (button) button.innerText = "Start Recording";
    }
}

function uploadRecording() {
    fetch('http://localhost:5000/get_audio')
    .then(response => response.json())
    .then(data => {
        if (data.audio) {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: data.audio,
            }, '*');
        }
    })
    .catch((error) => console.error('Error:', error));
}

// Streamlit event listener
window.addEventListener('message', function(event) {
    if (event.data.type === 'streamlit:render') {
        const startStopButton = window.parent.document.querySelector('button[kind="secondary"]:nth-of-type(1)');
        const uploadButton = window.parent.document.querySelector('button[kind="secondary"]:nth-of-type(2)');
        
        if (startStopButton && uploadButton) {
            startStopButton.addEventListener('click', toggleRecording);
            uploadButton.addEventListener('click', uploadRecording);
        }
    }
});
</script>
"""

# Inject JavaScript code
st.components.v1.html(js_code, height=0)

# Handle the uploaded audio data
if "audio_data" in st.session_state:
    audio_bytes = base64.b64decode(st.session_state.audio_data)
    audio_player.audio(audio_bytes, format="audio/wav")
    del st.session_state.audio_data  # Clear the audio data after playing

if start_stop_button:
    st.write("Click 'Upload Recording' when you're done to play the audio.")

if upload_button:
    st.write("Uploading recording... If you don't hear audio, please try recording again.")

# This will catch the audio data sent from JavaScript
if st.session_state.get("audio_data"):
    st.experimental_rerun()
