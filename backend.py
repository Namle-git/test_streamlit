from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Use a default path if HOME environment variable is not set
UPLOAD_FOLDER = os.path.join(os.environ.get('HOME', os.getcwd()), 'site', 'wwwroot', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/upload', methods=['POST'])
def upload_audio():
    app.logger.debug("Upload route hit")
    if 'audio' not in request.files:
        app.logger.error("No audio file provided")
        return jsonify({"error": "No audio file provided"}), 400
    audio = request.files['audio']
    audio_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    audio.save(audio_path)
    app.logger.debug(f"Audio saved to {audio_path}")
    return jsonify({"message": "Audio uploaded successfully", "path": audio_path})

@app.route('/set_path', methods=['POST'])
def set_path():
    data = request.get_json()
    path = data.get('path')
    with open(os.path.join(UPLOAD_FOLDER, 'audio_path.txt'), 'w') as f:
        f.write(path)
    app.logger.debug(f"Path set to {path}")
    return 'Path received', 200

@app.route('/test', methods=['GET'])
def test():
    app.logger.debug("Test route hit")
    return jsonify({"message": "CORS is working!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Listen on all network interfaces
