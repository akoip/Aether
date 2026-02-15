
# Main Assistant Python Script
import pyttsx3
import speech_recognition as sr
import subprocess
import openai
import random

# Initialize speech engine and GPT API
openai.api_key = 'your-api-key'
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Sample function to recognize speech
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio)
            print(f"Recognized command: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Speech recognition service unavailable.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

# Sample function to open application
def open_application(command):
    application_mappings = {
        "chrome": "chrome",
        "libreoffice": "libreoffice",
        "notepad": "notepad",
    }
    for app_name, app_command in application_mappings.items():
        if app_name in command:
            subprocess.run([app_command])
            speak(f"Opening {app_name}.")
            return
    speak("Application not recognized.")

# Main execution loop
while True:
    command = listen_for_command()
    if "open" in command:
        open_application(command)
    elif "exit" in command:
        speak("Goodbye.")
        break
