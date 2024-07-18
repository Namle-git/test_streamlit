from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
CORS(app)

@app.route('/save_audio', methods=['POST'])
def save_audio():
    audio_data = request.json['audio']
    audio_binary = base64.b64decode(audio_data.split(',')[1])
    
    # Save the audio file
    with open('recorded_audio.wav', 'wb') as f:
        f.write(audio_binary)
    
    return jsonify({"message": "Audio saved successfully"})

@app.route('/get_audio', methods=['GET'])
def get_audio():
    if os.path.exists('recorded_audio.wav'):
        with open('recorded_audio.wav', 'rb') as f:
            audio_binary = f.read()
        audio_base64 = base64.b64encode(audio_binary).decode('utf-8')
        return jsonify({"audio": audio_base64})
    else:
        return jsonify({"error": "No audio file found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)
