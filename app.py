import streamlit as st
import streamlit.components.v1 as components

html_code = """
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
    
        fetch('https://simonaireceptionistchatbot.azurewebsites.net/flask/upload', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            if (data.path) {
                fetch('https://simonaireceptionistchatbot.azurewebsites.net/flask/set_path', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: data.path })
                }).then(() => {
                    alert('Audio uploaded and path set successfully');
                });
            } else {
                alert('Audio upload failed');
            }
        }).catch(error => {
            console.error('Upload error:', error);
        });
    
        document.getElementById('upload').disabled = true;
        audioChunks = [];  // Reset the audio chunks for the next recording
    }
    
    // Test fetch
    fetch('https://simonaireceptionistchatbot.azurewebsites.net/flask/test', {
        method: 'GET'
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        alert(data.message);
    }).catch(error => {
        console.error('Test fetch error:', error);
    });
</script>

<button id="record" onclick="startRecording()">Record</button>
<button id="stop" onclick="stopRecording()" disabled>Stop</button>
<button id="upload" onclick="uploadAudio()" disabled>Upload</button>
<audio id="audio" controls></audio>
"""

components.html(html_code, height=600)
