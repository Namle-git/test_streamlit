import streamlit as st
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import base64
import os
from io import BytesIO
from threading import Thread
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Flask server setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://simonaireceptionistchatbot.azurewebsites.net"}})
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_audio():
    logging.debug("Received audio upload request")
    try:
        data = request.get_json()
        audio_base64 = data['audio'].split(',')[1]  # Remove the data URL scheme
        audio_data = base64.b64decode(audio_base64)
        
        # Save the audio data to a file
        audio_id = 'recording.wav'
        audio_path = os.path.join(UPLOAD_FOLDER, audio_id)
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(audio_data)
        
        logging.debug("Audio uploaded successfully")
        return jsonify({'message': 'Audio uploaded successfully', 'audio_id': audio_id})
    except Exception as e:
        logging.error(f"Error uploading audio: {e}")
        return jsonify({'message': 'Error uploading audio', 'error': str(e)}), 500

@app.route('/get_audio/<audio_id>', methods=['GET'])
def get_audio(audio_id):
    logging.debug("Received get audio request")
    audio_path = os.path.join(UPLOAD_FOLDER, audio_id)
    if not os.path.exists(audio_path):
        return "Audio not found", 404

    logging.debug("Sending audio file")
    return send_file(audio_path, mimetype='audio/wav', as_attachment=True, attachment_filename=audio_id)

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    run_flask()
