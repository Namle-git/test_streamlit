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

echo "Starting the Flask server..."
python3 ./backend.py
