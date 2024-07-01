#!/bin/bash

echo "Updating package list..."
apt-get update

echo "Installing required libraries..."
apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

echo "Installing PyAudio..."
pip install PyAudio==0.2.14

echo "Updating the shared library cache..."
ldconfig

echo "Starting the Streamlit app..."
# Start Streamlit app and redirect logs to streamlit.log
streamlit run app.py --server.port $PORT > streamlit.log 2>&1
