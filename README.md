# RaspberryPi_chatbot

1. System Update and Python installation
sudo apt-get update
sudo apt-get upgrade
python3 --version
2. Package Installation
sudo apt-get install python3-pip
sudo apt-get install portaudio19-dev python3-pyaudio 
pip3 install pyaudio
pip3 install SpeechRecognition pyttsx3 gtts python-dotenv
pip install openai
sudo apt-get install espeak
sudo apt-get install Flac

4. Testing Hardware.
 a. Test Microphone
    arecord --format=S16_LE --duration=5 --rate=16000 --file-type=wav test_mic.wav aplay test_mic.wav speaker-test -t wav
5. Environment Variables.
OPENAI_API_KEY=’your_key’

