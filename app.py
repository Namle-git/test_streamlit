import streamlit as st
import base64
from io import BytesIO
from pydub import AudioSegment
import streamlit.components.v1 as components
import time

st.title("Audio Recorder in Streamlit")

# Initialize session state for audio data
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = ""

# Initialize session state for audio data
if 'query_params' not in st.session_state:
    st.session_state.query_params = ""


st.write("This is the query_params")
st.write(st.session_state.query_params)

st.session_state.query_params = "hello"
# Display the Base64 string if available
if st.session_state.audio_data:
    st.write("Base64 Audio Data:")
    st.write(st.session_state.audio_data)

