import streamlit as st
import base64
from io import BytesIO
from pydub import AudioSegment
import streamlit.components.v1 as components
import time

st.title("Audio Recorder in Streamlit")

# Initialize session state for audio data
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = ""

# Initialize session state for audio data
if 'query_params' not in st.session_state:
    st.session_state.query_params = ""

# JavaScript for audio recording and setting session state
record_audio_html = """
<button onclick="startRecording()">Start Recording</button>
<input type="hidden" id="audio_data" name="audio_data" onchange="handleAudioDataChange()">

<script>
let mediaRecorder;
let audioChunks = [];

// Function to start recording audio
function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];  // Reset audio chunks
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
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
            mediaRecorder.start();

            // Automatically stop recording after 5 seconds (5000 milliseconds)
            setTimeout(() => {
                if (mediaRecorder.state !== "inactive") {
                    mediaRecorder.stop();
                }
            }, 5000);
        });
}

function handleAudioDataChange() {
    const audioDataInput = document.getElementById("audio_data").value;
    const audioDataEvent = new CustomEvent("audioDataAvailable", { detail: { audioData: audioDataInput } });
    window.dispatchEvent(audioDataEvent);
}

window.addEventListener("audioDataAvailable", (event) => {
    const audioData = event.detail.audioData;
    updateURLWithAudioData(audioData);
});

function updateURLWithAudioData(base64Audio) {
    const currentURL = new URL(window.location.href);
    currentURL.searchParams.set('audio_upload', base64Audio);
    window.history.replaceState({}, '', currentURL);
}
</script>
"""

components.html(record_audio_html, height=200)

# Function to handle the custom event and update session state
def handle_audio_data():
    audio_data = st.session_state.audio_data
    if audio_data:
        audio_bytes = base64.b64decode(audio_data)
        audio = AudioSegment.from_file(BytesIO(audio_bytes), format="wav")
        st.audio(BytesIO(audio_bytes), format='audio/wav')
        st.write("Audio recorded successfully!")

if st.button("GET audio"):
    # Capture query parameters sent by the JavaScript
    query_params = st.query_params.to_dict()
    st.session_state.query_params=query_params
    st.write("This is the query_params")
    st.write(st.session_state.query_params)
    
    st.write("This is the audio_data")
    if "audio_data" in query_params:
        st.session_state.audio_data = query_params["audio_data"][0]
    
    # Display the Base64 string if available
    if st.session_state.audio_data:
        st.write("Base64 Audio Data:")
        st.write(st.session_state.audio_data)
