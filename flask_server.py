from flask import Flask, request, jsonify
import speech_recognition as sr
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    data = request.get_json()
    audio_base64 = data['audio'].split(',')[1]  # Remove the data URL scheme
    audio_data = base64.b64decode(audio_base64)
    
    recognizer = sr.Recognizer()
    audio_file = BytesIO(audio_data)
    
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        transcription = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        transcription = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        transcription = f"Could not request results from Google Speech Recognition service; {e}"
    
    return jsonify({'transcription': transcription})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
