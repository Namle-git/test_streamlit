#!/bin/bash

echo "Updating package list..."
apt-get update

echo "Installing required libraries..."
apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

echo "Installing PyAudio..."
pip install PyAudio==0.2.14

echo "Updating the shared library cache..."
ldconfig

echo "Starting the Flask backend server with waitress..."
# Start Flask backend server with waitress on port 8000
python backend.py > flask.log 2>&1 &

echo "Starting the Streamlit app..."
# Start Streamlit app and redirect logs to streamlit.log
streamlit run app.py --server.port 8000 > streamlit.log 2>&1
