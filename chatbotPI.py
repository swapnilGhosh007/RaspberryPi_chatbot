import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np

# Load API key from environment variable
load_dotenv()
openai.api_key = os.getenv('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')
model = 'gpt-3.5-turbo'

# Initialize the speech recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[0]  # Adjust index based on the voice preference
engine.setProperty('voice', voice.id)

# Bot's name
bot_name = "Echo"

# Define greetings
name = "Nafee"
greetings = [
    f"Hi there, I'm {bot_name}. What can I do for you today?",
    f"Hello! {bot_name} at your service. How can I assist?",
    f"Greetings from {bot_name}! How may I help you today?",
    f"It's a great day to chat! What's on your mind?"
]

def listen_for_wake_word(source):
    print(f"Listening for 'Hey {bot_name}'...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if f"hey {bot_name}".lower() in text.lower():
                print(f"Wake word detected for {bot_name}.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
        except sr.UnknownValueError:
            pass  # Do nothing if the speech was not recognized

def listen_and_respond(source):
    print("Listening...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if text:
                print(f"You said: {text}")
                response = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": f"{text}"}])
                response_text = response.choices[0].message.content
                print(f"{bot_name} says: {response_text}")
                engine.say(response_text)
                engine.runAndWait()
        except sr.UnknownValueError:
            time.sleep(2)
            print(f"{bot_name} is listening again...")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"{bot_name} could not request results; {e}")
            engine.runAndWait()

# Start the application
with sr.Microphone() as source:
    listen_for_wake_word(source)
