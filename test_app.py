import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import speech_recognition as sr
import av
import numpy as np

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to recognize speech using SpeechRecognition package
def recognize_speech(audio_data):
    try:
        audio = sr.AudioFile(audio_data)
        with audio as source:
            recognizer.adjust_for_ambient_noise(source)
            data = recognizer.record(source)
        text = recognizer.recognize_google(data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

# Custom class to process audio frames
class AudioProcessor:
    def __init__(self):
        self.audio_data = None

    def recv(self, frame):
        audio_frame = frame.to_ndarray().flatten().astype(np.int16)
        self.audio_data = av.AudioFrame.from_ndarray(audio_frame, layout='mono').to_bytes()
        return frame

# Streamlit WebRTC setup
st.title("Speech Recognition with Streamlit")

# WebRTC client settings
client_settings = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"audio": True, "video": False},
)

# Instantiate webrtc_streamer with audio processor
audio_processor = AudioProcessor()
webrtc_ctx = webrtc_streamer(
    key="speech-recognition",
    mode=WebRtcMode.SENDRECV,
    client_settings=client_settings,
    audio_processor_factory=lambda: audio_processor,
)

# Process audio data if available
if webrtc_ctx.state.playing:
    if audio_processor.audio_data:
        st.spinner('Listening...')
        result = recognize_speech(audio_processor.audio_data)
        with st.chat_message("user"):
            st.markdown(result)
        # Reset the audio data
        audio_processor.audio_data = None
