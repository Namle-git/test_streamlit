#!/bin/bash

echo "Updating package list..."
apt-get update

echo "Installing required libraries..."
apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

echo "Installing PyAudio..."
pip install PyAudio==0.2.14

echo "Updating the shared library cache..."
ldconfig

echo "Starting the integrated Flask and Streamlit server..."
# Start Flask backend server in the background and redirect logs to backend.log
nohup python backend.py > backend.log 2>&1 &
