import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings

# Set up the title of the app
st.title("Microphone Access Request")

# Add some description
st.write("This app requires access to your microphone. Please grant permission to continue.")

# Define the WebRTC client settings
WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"audio": True, "video": False},
)

# Set up the WebRTC streamer
webrtc_ctx = webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,
    client_settings=WEBRTC_CLIENT_SETTINGS,
    async_processing=True,
)

if webrtc_ctx.state.playing:
    st.write("Microphone access granted.")
else:
    st.write("Click the start button to request microphone access.")
