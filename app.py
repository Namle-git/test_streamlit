import streamlit as st
import base64
from io import BytesIO
from pydub import AudioSegment

st.title("Audio Recorder in Streamlit")

# Initialize session state for audio data
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = ""

# JavaScript for audio recording and setting session state
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
            const audioDataInput = document.getElementById("audio_data");
            audioDataInput.value = base64String;
            audioDataInput.dispatchEvent(new Event('change'));
        };
    };
}
</script>
<button onclick="startRecording()">Start Recording</button>
<button onclick="stopRecording()">Stop Recording</button>
<input type="hidden" id="audio_data" name="audio_data" oninput="updateAudioData()">
<script>
function updateAudioData() {
    const audioDataInput = document.getElementById("audio_data");
    if (audioDataInput.value) {
        fetch('/update_audio_data', {
            method: 'POST',
            body: JSON.stringify({ audio: audioDataInput.value }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }
}
</script>
"""

st.components.v1.html(record_audio_html)

# Function to handle audio data update via session state
def update_audio_data(audio_data):
    st.session_state.audio_data = audio_data

# Process and display the audio data if available
if st.session_state.audio_data:
    audio_bytes = base64.b64decode(st.session_state.audio_data)
    audio = AudioSegment.from_file(BytesIO(audio_bytes), format="wav")
    st.audio(BytesIO(audio_bytes), format='audio/wav')

    # Process the audio object as needed
    st.write("Audio recorded successfully!")
