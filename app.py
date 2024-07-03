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
<input type="hidden" id="audio_data" name="audio_data" onchange="handleAudioDataChange()">
<script>
function handleAudioDataChange() {
    const audioDataInput = document.getElementById("audio_data").value;
    const audioDataEvent = new CustomEvent("audioDataAvailable", { detail: { audioData: audioDataInput } });
    window.dispatchEvent(audioDataEvent);
}
window.addEventListener("audioDataAvailable", (event) => {
    const audioData = event.detail.audioData;
    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ audio_data: audioData }),
    }).then(() => window.location.reload());
});
</script>
"""

st.components.v1.html(record_audio_html)

# Function to handle the custom event and update session state
def handle_audio_data():
    audio_data = st.session_state.audio_data
    if audio_data:
        audio_bytes = base64.b64decode(audio_data)
        audio = AudioSegment.from_file(BytesIO(audio_bytes), format="wav")
        st.audio(BytesIO(audio_bytes), format='audio/wav')
        st.write("Audio recorded successfully!")

# Check for POST request to update session state
if st.request.method == "POST":
    request_data = st.request.get_json()
    st.session_state.audio_data = request_data.get("audio_data", "")
    handle_audio_data()

# Display the recorded audio if available
if st.session_state.audio_data:
    handle_audio_data()
