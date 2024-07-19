from flask import Flask, request, jsonify, send_file
import os
import base64
import threading
import streamlit as st
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Flask app
flask_app = Flask(__name__)

@flask_app.route('/api/save_audio', methods=['POST'])
def save_audio():
    audio_data = request.json['audio']
    audio_binary = base64.b64decode(audio_data.split(',')[1])
    
    # Save the audio file
    with open('recorded_audio.wav', 'wb') as f:
        f.write(audio_binary)
    
    return jsonify({"message": "Audio saved successfully"})

@flask_app.route('/api/get_audio', methods=['GET'])
def get_audio():
    if os.path.exists('recorded_audio.wav'):
        return send_file('recorded_audio.wav', mimetype='audio/wav')
    else:
        return jsonify({"error": "No audio file found"}), 404

# Streamlit app
def streamlit_app():
    st.title("Audio Recorder and Player")

    # Placeholder for audio player
    audio_player = st.empty()

    # Create buttons
    col1, col2 = st.columns(2)
    start_stop_button = col1.button("Start Recording", key="start_stop")
    upload_button = col2.button("Upload Recording", key="upload")

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
                    fetch('/api/save_audio', {
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

    // Streamlit event listener
    window.addEventListener('message', function(event) {
        if (event.data.type === 'streamlit:render') {
            const startStopButton = window.parent.document.querySelector('button[kind="secondary"]:nth-of-type(1)');
            if (startStopButton) {
                startStopButton.addEventListener('click', toggleRecording);
            }
        }
    });
    </script>
    """

    # Inject JavaScript code
    st.components.v1.html(js_code, height=0)

    if start_stop_button:
        st.write("Click 'Start Recording' again to stop recording.")

    if upload_button:
        with open('recorded_audio.wav', 'rb') as f:
            audio_bytes = f.read()
        audio_player.audio(audio_bytes, format="audio/wav")

# Combine Flask and Streamlit apps
def create_app():
    from streamlit.web import cli as stcli

    def run_streamlit():
        stcli._main_run_clExplicitRequestIndik("app.py", args=[])

    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.start()

    return DispatcherMiddleware(flask_app, {
        '/streamlit': lambda e, s: run_simple('localhost', 8501, streamlit_app)
    })

app = create_app()

if __name__ == '__main__':
    app.run(port=8000)
