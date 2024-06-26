import streamlit as st
import speech_recognition as sr
import tempfile

# Function to record audio
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Recording...")
        audio = recognizer.listen(source)
        st.write("Recording stopped.")
        
        return audio

# Function to transcribe audio
def transcribe_audio(audio):
    recognizer = sr.Recognizer()
    try:
        st.write("Transcribing audio...")
        text = recognizer.recognize_google(audio)
        st.write("Transcription successful.")
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

st.title("Speech Recognition App")
st.write("Click the button below to record audio and transcribe it.")

if st.button("Record Audio"):
    audio = record_audio()
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(audio.get_wav_data())
        st.audio(temp_audio.name, format='audio/wav')
    
    transcription = transcribe_audio(audio)
    st.write("Transcription:")
    st.write(transcription)
