import streamlit as st
import speech_recognition as sr
import os
from pydub import AudioSegment
import tempfile
import requests

st.title("Speech Recognition App")

# Frontend HTML and JavaScript
st.write("""
    <script>
        const startRecording = () => {
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    const mediaRecorder = new MediaRecorder(stream);
                    let audioChunks = [];

                    mediaRecorder.ondataavailable = event => {
                        audioChunks.push(event.data);
                    };

                    mediaRecorder.onstop = () => {
                        const audioBlob = new Blob(audioChunks);
                        const audioUrl = URL.createObjectURL(audioBlob);
                        const audio = new Audio(audioUrl);
                        audio.play();

                        const reader = new FileReader();
                        reader.readAsDataURL(audioBlob);
                        reader.onloadend = () => {
                            const base64String = reader.result.split(',')[1];
                            fetch('/audio', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({ audio: base64String }),
                            }).then(response => response.json())
                              .then(data => {
                                  console.log(data);
                                  document.getElementById('transcription').innerText = data.transcription;
                              });
                        };
                    };

                    mediaRecorder.start();

                    setTimeout(() => {
                        mediaRecorder.stop();
                    }, 5000); // Record for 5 seconds
                });
        };
    </script>
""", unsafe_allow_html=True)

# Button to start recording
if st.button("Record"):
    st.write("<script>startRecording();</script>", unsafe_allow_html=True)

st.write("<div id='transcription'></div>", unsafe_allow_html=True)
