from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.environ['HOME'], 'site', 'wwwroot', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    audio = request.files['audio']
    audio_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    audio.save(audio_path)
    return jsonify({"message": "Audio uploaded successfully", "path": audio_path})

@app.route('/set_path', methods=['POST'])
def set_path():
    data = request.get_json()
    path = data.get('path')
    with open(os.path.join(UPLOAD_FOLDER, 'audio_path.txt'), 'w') as f:
        f.write(path)
    return 'Path received', 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
