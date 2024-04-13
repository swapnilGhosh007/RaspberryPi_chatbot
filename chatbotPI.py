import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
from gtts import gTTS
import playsound

# Load API key from environment variable
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model = 'gpt-3.5-turbo'  # You can change to 'gpt-4' or another model as preferred

# Initialize the speech recognizer
r = sr.Recognizer()

# Bot's name
bot_name = "Friday"

# Define greetings
name = "Nafee"
greetings = [
    f"Hi there, I'm {bot_name}. What can I do for you today?",
    f"Hello! {bot_name} at your service. How can I assist?",
    f"Greetings from {bot_name}! How may I help you today?",
    f"It's a great day to chat! What's on your mind?"
]

def speak(text):
    """Use Google Text-to-Speech for output."""
    tts = gTTS(text=text, lang='en', slow=False)
    filename = "temp.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def listen_for_wake_word(source):
    """Listen for the wake word and respond."""
    print(f"Listening for 'Hey {bot_name}'...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if f"hey {bot_name}".lower() in text.lower():
                print(f"Wake word detected for {bot_name}.")
                speak_response(np.random.choice(greetings))
                listen_and_respond(source)
        except sr.UnknownValueError:
            pass  # Do nothing if the speech was not recognized

def listen_and_respond(source):
    """Listen for user input and respond via ChatGPT."""
    print("Listening...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if text:
                print(f"You said: {text}")
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": text}],
                    max_tokens=60,
                    temperature=0.5
                )
                response_text = response.choices[0].message["content"]
                print(f"{bot_name} says: {response_text}")
                speak_response(response_text)
        except sr.UnknownValueError:
            time.sleep(2)
            print(f"{bot_name} is listening again...")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak_response(f"{bot_name} could not request results; {e}")

def speak_response(text):
    """Speak the response text."""
    print("Speaking:", text)
    speak(text)

# Start the application
if __name__ == "__main__":
    with sr.Microphone() as source:
        listen_for_wake_word(source)
