import streamlit as st
import base64

st.title("Audio Recorder and Player")

# Placeholder for audio player
audio_player = st.empty()

# Create buttons
col1, col2, col3 = st.columns(3)
start_button = col1.button("Start Recording")
stop_button = col2.button("Stop Recording")
upload_button = col3.button("Upload Recording")

# Hidden form for audio data
with st.form(key='audio_form', clear_on_submit=True):
    audio_data_input = st.text_input("Audio Data", key="audio_data_input", type="password")
    submitted = st.form_submit_button("Submit Audio", type="primary")
    if submitted:
        audio_data = audio_data_input.split(",")[1]  # Remove the "data:audio/wav;base64," prefix
        audio_bytes = base64.b64decode(audio_data)
        st.session_state.audio_bytes = audio_bytes

# JavaScript to handle audio recording
js_code = """
<script>
let mediaRecorder;
let audioChunks = [];

function startRecording() {
    audioChunks = [];
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });
        });
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = () => {
                const base64data = reader.result;
                document.getElementById('audio_data_input').value = base64data;
            }
        });
    }
}

function uploadRecording() {
    document.querySelector('form button[type="submit"]').click();
}

// Streamlit Streamlit event listener
window.addEventListener('message', function(event) {
    if (event.data.type === 'streamlit:render') {
        const startButton = window.parent.document.querySelector('button[kind="secondary"]:nth-of-type(1)');
        const stopButton = window.parent.document.querySelector('button[kind="secondary"]:nth-of-type(2)');
        const uploadButton = window.parent.document.querySelector('button[kind="secondary"]:nth-of-type(3)');
        
        if (startButton && stopButton && uploadButton) {
            startButton.addEventListener('click', startRecording);
            stopButton.addEventListener('click', stopRecording);
            uploadButton.addEventListener('click', uploadRecording);
        }
    }
});
</script>
"""

# Inject JavaScript code
st.components.v1.html(js_code, height=0)

# Handle the uploaded audio data
if "audio_bytes" in st.session_state and st.session_state.audio_bytes:
    audio_player.audio(st.session_state.audio_bytes, format="audio/wav")
    st.session_state.audio_bytes = None  # Clear the audio data after playing

if start_button:
    st.write("Recording started. Click 'Stop Recording' when you're done.")

if stop_button:
    st.write("Recording stopped. Click 'Upload Recording' to play the audio.")

if upload_button:
    st.write("Uploading recording... If you don't hear audio, please try recording again.")
