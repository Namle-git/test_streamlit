import streamlit as st
import base64

# Initialize Streamlit app
st.title("Audio Recording Web App")

# Initialize session state for audio
if "audio_data" not in st.session_state:
    st.session_state["audio_data"] = None

# HTML and JavaScript for recording audio with a button
html_code = """
<script>
console.log("Script loaded");

var mediaRecorder;
var audioChunks = [];

function startRecording() {
    console.log("Starting recording...");
    document.getElementById("status").innerText = "Recording...";
    document.getElementById("status").style.color = "red";

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            console.log("Microphone access granted");
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            console.log("MediaRecorder started");

            mediaRecorder.addEventListener("dataavailable", event => {
                console.log("Data available event: ", event);
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                console.log("Recording stopped");
                var audioBlob = new Blob(audioChunks);
                var reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = function() {
                    var base64data = reader.result.split(',')[1];
                    console.log("Audio data read as base64");

                    fetch('/audio_upload', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ audio: base64data })
                    }).then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok: ' + response.statusText);
                        }
                        return response.json();
                    }).then(data => {
                        console.log("Received response:", data);
                        document.getElementById("status").innerText = "Recording stopped";
                        document.getElementById("status").style.color = "black";
                    }).catch(error => {
                        console.error("Error uploading audio:", error);
                        document.getElementById("status").innerText = "Error uploading audio: " + error.message;
                        document.getElementById("status").style.color = "red";
                    });
                }
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // Record for 5 seconds
        }).catch(error => {
            console.error("Error accessing microphone:", error);
            document.getElementById("status").innerText = "Error accessing microphone: " + error.message;
            document.getElementById("status").style.color = "red";
        });
}

document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM content loaded");
    document.getElementById("startButton").addEventListener("click", startRecording);
});
</script>

<button id="startButton">Start Recording</button>
<p id="status">Status: Not recording</p>
"""

# Include the HTML and JavaScript in the Streamlit app
st.components.v1.html(html_code, height=300)

# Create an endpoint in Streamlit to receive the audio data
def audio_upload_handler():
    from flask import request
    data = request.json
    st.session_state["audio_data"] = base64.b64decode(data['audio'])
    return "Audio received", 200

# Run the Streamlit app with the Flask endpoint
from streamlit.components.v1 import declare_component
import streamlit.components.v1 as components

def main():
    # Use Flask to handle the POST request
    from flask import Flask, request
    app = Flask(__name__)
    app.add_url_rule('/audio_upload', 'audio_upload', audio_upload_handler, methods=['POST'])

    # Run Flask in a separate thread
    from threading import Thread
    thread = Thread(target=app.run, kwargs={'port': 8501})
    thread.start()

    # Your Streamlit code
    st.title("Streamlit App with Audio Recording")

    # Add the JavaScript and HTML code
    st.components.v1.html(html_code, height=300)

    # Display the recorded audio if available
    if st.session_state["audio_data"]:
        st.audio(st.session_state["audio_data"], format="audio/wav")

if __name__ == "__main__":
    main()
