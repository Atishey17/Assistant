import openai
import pyttsx3
from gtts import gTTS
import streamlit as st
import os
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

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response["choices"][0]["message"]["content"]

def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("input.wav")
    os.system("start input.wav")

def main():
    st.title("Voice Assistant with Streamlit")

    selected_language = st.sidebar.selectbox("Select Language", ["en", "es", "fr", "hi", "de", "ru", "pt", "ja", "it", "ar"])

    language_name = language_details[selected_language]["name"]
    st.sidebar.markdown(f"**Language Details**\n\n**Name:** {language_name}")

    user_input = st.text_input("Type your question:")

    messages = []
    if st.button("Submit"):
        messages.append(f"You typed: {user_input}")

        response = generate_response(user_input)
        messages.append(f"AI says: {response}")

        speak_text(response, lang=selected_language)

    if st.sidebar.button("Input by typing", key="input_by_typing"):
        webbrowser.open("http://www.google.com", new=2)

    for message in messages:
        st.text(message)

if __name__ == "__main__":
    main()