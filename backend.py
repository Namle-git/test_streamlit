import streamlit as st
from flask import Flask, request, jsonify, send_file
import base64
import os
from io import BytesIO
from threading import Thread
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Flask server setup
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_audio():
    logging.debug("Received audio upload request")
    data = request.get_json()
    audio_base64 = data['audio'].split(',')[1]  # Remove the data URL scheme
    audio_data = base64.b64decode(audio_base64)
    
    # Save the audio data to a file
    audio_id = 'recording.wav'
    audio_path = os.path.join(UPLOAD_FOLDER, audio_id)
    with open(audio_path, 'wb') as audio_file:
        audio_file.write(audio_data)
    
    logging.debug("Audio uploaded successfully")
    # Return the audio ID
    return jsonify({'message': 'Audio uploaded successfully', 'audio_id': audio_id})

@app.route('/get_audio/<audio_id>', methods=['GET'])
def get_audio(audio_id):
    logging.debug("Received get audio request")
    audio_path = os.path.join(UPLOAD_FOLDER, audio_id)
    if not os.path.exists(audio_path):
        return "Audio not found", 404

    logging.debug("Sending audio file")
    return send_file(audio_path, mimetype='audio/wav', as_attachment=True, attachment_filename=audio_id)

def run_flask():
    app.run(port=5000, debug=True, use_reloader=False)

# Note: Do not start the thread here. This will be done in the main Streamlit app file.
