from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import speech_recognition as sr
from pydub import AudioSegment
import io

app = Flask(__name__)
CORS(app)

@app.route('/audio', methods=['POST'])
def audio():
    data = request.json
    audio_base64 = data['audio']
    audio_data = base64.b64decode(audio_base64)

    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_wav:
        audio_segment.export(tmp_wav.name, format="wav")
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_wav.name) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                return jsonify({"transcription": text})
            except sr.UnknownValueError:
                return jsonify({"transcription": "Google Speech Recognition could not understand audio"})
            except sr.RequestError as e:
                return jsonify({"transcription": f"Could not request results; {e}"})
    finally:
        os.remove(tmp_wav.name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
