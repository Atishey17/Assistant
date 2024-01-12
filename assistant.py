import openai
import pyttsx3
import speech_recognition as sr
import os
from gtts import gTTS
import streamlit as st
import webbrowser

api_key = "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"
openai.api_key = api_key

engine = pyttsx3.init()

language_details = {
    "en": {"name": "English"},
    "es": {"name": "Spanish"},
    "fr": {"name": "French"},
    "hi": {"name": "Hindi"},
    "de": {"name": "German"},
    "ru": {"name": "Russian"},
    "pt": {"name": "Portuguese"},
    "ja": {"name": "Japanese"},
    "it": {"name": "Italian"},
    "ar": {"name": "Arabic"},
}
def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print("Skipping unknown error")

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response["choices"][0]["message"]["content"]

def speak_text_with_gtts(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3")

def main():
    st.title("Voice Assistant with Streamlit")

    selected_language = st.sidebar.selectbox("Select Language", ["en", "es", "fr", "hi", "de", "ru", "pt", "ja", "it", "ar"])

    speech_speed = st.sidebar.slider("Select Speech Speed", min_value=50, max_value=300, value=200)

    if st.sidebar.button("Input by typing", key="input_by_typing"):
        webbrowser.open("http://www.google.com", new=2)

    while True:
        st.write("Say 'hello' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hello":
                    os.system("entry.mp3")
                    filename = "input.wav"
                    st.write("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(
                            source, phrase_time_limit=None, timeout=None
                        )
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    text = transcribe_audio_to_text(filename)
                    if text:
                        st.write(f"You said: {text}")

                        response = generate_response(text)
                        st.write(f"AI says: {response}")

                        speak_text_with_gtts(response, lang=selected_language)
            except Exception as e:
                st.write(f"Error occurred: {e}")

if __name__ == "__main__":
    main()