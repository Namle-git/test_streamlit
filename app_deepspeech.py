import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.samplerate = 44100

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Example of processing audio frame
        # Here you can modify the frame, apply filters, etc.
        return frame

webrtc_ctx = webrtc_streamer(
    key="example",
    mode="sendrecv",
    client_settings=ClientSettings(
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    ),
    audio_processor_factory=AudioProcessor,
)

if webrtc_ctx.state.playing:
    st.write("Streaming audio...")

st.write("This is an audio-only Streamlit-WeRTC app.")
