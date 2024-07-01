#!/bin/bash

# Update package list and install required libraries
apt-get update
apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

# Install PyAudio
pip install PyAudio==0.2.14

# Update the shared library cache
ldconfig

# Start the Flask backend server in the background
python backend.py &

# Start the Streamlit app
streamlit run app.py --server.port $PORT
