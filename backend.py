from flask import Flask, request, jsonify
import base64
import speech_recognition as sr
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route('/audio', methods=['POST'])
def audio():
    data = request.json
    audio_base64 = data['audio']
    audio_data = base64.b64decode(audio_base64)

    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
    audio_segment.export("audio.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return jsonify({"transcription": text})
        except sr.UnknownValueError:
            return jsonify({"transcription": "Google Speech Recognition could not understand audio"})
        except sr.RequestError as e:
            return jsonify({"transcription": f"Could not request results; {e}"})

if __name__ == '__main__':
    app.run()
