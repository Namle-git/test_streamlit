import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.samplerate = 44100

    def recv(self, frame):
        # Here you can add your audio processing code
        return frame

webrtc_streamer(
    key="example",
    mode="sendrecv",
    client_settings=ClientSettings(
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    ),
    audio_processor_factory=AudioProcessor,
)

st.write("This is an audio-only Streamlit-WeRTC app.")
