import speech_recognition as sr
import pyttsx3
import openai

# Initializing pyttsx3
listening = True
engine = pyttsx3.init()

# Set your OpenAI API key and customize the ChatGPT role
openai.api_key = "xyz"
messages = [{"role": "system", "content": "Your name is Friday and give answers in 2 lines"}]

# Customizing the output voice
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')


def get_response(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply


while listening:
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000

        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5.0)
            response = recognizer.recognize_google(audio)
            print(response)
           
            if "friday" in response.lower():
                response_from_openai = get_response(response)
                engine.setProperty('rate', 120)  # Adjusting the speech rate
                engine.setProperty('volume', volume)  # Setting the volume
                engine.setProperty('voice', 'greek')  # Assuming the first voice is the desired one; adjust as needed
                engine.say(response_from_openai)
                engine.runAndWait()
            else:
                print("Didn't recognize 'Friday'.")
           
        except sr.UnknownValueError:
            print("Didn't recognize anything.")
