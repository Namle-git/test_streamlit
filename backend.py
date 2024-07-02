import io
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    data = request.json['audio']
    # Decode the base64 string
    audio_data = base64.b64decode(data.split(',')[1])

    # Save audio data to memory
    audio_file = io.BytesIO(audio_data)

    # Here, you can process the audio data in memory as needed
    # For example, you might want to save it to a database, or perform some analysis on it

    response = {
        'audio_id': 'unique_audio_id',  # Replace with actual ID or identifier
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
