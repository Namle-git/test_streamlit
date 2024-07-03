#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status.

echo "Updating package list..."
apt-get update || { echo "Failed to update package list"; exit 1; }

echo "Installing required libraries..."
apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 || { echo "Failed to install required libraries"; exit 1; }

echo "Installing PyAudio..."
pip install PyAudio==0.2.14 || { echo "Failed to install PyAudio"; exit 1; }

echo "Updating the shared library cache..."
ldconfig || { echo "Failed to update shared library cache"; exit 1; }

echo "Starting the integrated Flask and Streamlit server..."

# Ensure PORT and WEBSITES_PORT are set
export PORT=${PORT:-8000}
export WEBSITES_PORT=${WEBSITES_PORT:-8501}

# Start Flask backend server in the background and redirect logs to backend.log
nohup python backend.py > backend.log 2>&1 &

echo "Startup script completed."
