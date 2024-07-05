import streamlit as st
import os
import streamlit.components.v1 as components

# Define the HTML and JavaScript for audio recording and uploading
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Recorder</title>
</head>
<body>
    <h1>Audio Recorder</h1>
    <button id="record" onclick="startRecording()">Record</button>
    <button id="stop" onclick="stopRecording()" disabled>Stop</button>
    <button id="upload" onclick="uploadAudio()" disabled>Upload</button>
    <audio id="audio" controls></audio>
    
    <script>
        let mediaRecorder;
        let audioChunks = [];

        async function startRecording() {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.start();
            document.getElementById('record').disabled = true;
            document.getElementById('stop').disabled = false;
        }

        function stopRecording() {
            mediaRecorder.stop();
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = document.getElementById('audio');
                audio.src = audioUrl;
                document.getElementById('upload').disabled = false;
            };
            document.getElementById('record').disabled = false;
            document.getElementById('stop').disabled = true;
        }

        function uploadAudio() {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');

            fetch('/flask/upload', {
                method: 'POST',
                body: formData
            }).then(response => response.json())
            .then(data => {
                if (data.path) {
                    fetch('/flask/set_path', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ path: data.path })
                    }).then(() => {
                        alert('Audio uploaded and path set successfully');
                    });
                } else {
                    alert('Audio upload failed');
                }
            });

            document.getElementById('upload').disabled = true;
            audioChunks = [];  // Reset the audio chunks for the next recording
        }
    </script>
</body>
</html>
"""

# Streamlit app layout
st.title("Audio Recorder and Processor")

# Render the HTML code in Streamlit
components.html(html_code, height=600)

def get_audio_path():
    upload_folder = os.path.join(os.environ['HOME'], 'site', 'wwwroot', 'uploads')
    path_file = os.path.join(upload_folder, 'audio_path.txt')
    try:
        with open(path_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
if st.button("Get audio")
    audio_path = get_audio_path()

if audio_path:
    st.audio(audio_path)
    st.write(f"Audio file path: {audio_path}")
    # Add your audio processing logic here
else:
    st.write("No audio file uploaded yet.")
