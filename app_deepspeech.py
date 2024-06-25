import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings, WebRtcMode

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.samplerate = 44100

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Example of processing audio frame
        return frame

WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"audio": True, "video": False},
)

webrtc_ctx = webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,
    client_settings=WEBRTC_CLIENT_SETTINGS,
    audio_processor_factory=AudioProcessor,
)

if webrtc_ctx.state.playing:
    st.write("Streaming audio...")

st.write("This is an audio-only Streamlit-WeRTC app.")
