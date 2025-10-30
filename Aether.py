
# Main Assistant Python Script
import pyttsx3
import speech_recognition as sr
import subprocess
import openai
import random
import requests
import urllib.parse

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
        audio = recognizer.listen(source)
        command = recognizer.recognize_google(audio)
        return command.lower()

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

# --- Weather helper ---
def get_weather(city: str | None = None) -> str:
    """
    Fetch a short weather summary from wttr.in.

    If city is None, wttr.in will return weather for the requester's IP (may be inaccurate).
    We request a short 1-line summary using the `format=3` parameter:
        <Location>: <condition>, <temp>

    Returns spoken text (and also prints it).
    """
    try:
        target = city.strip() if city else ""
        # URL-encode city (e.g., "New York" -> "New+York")
        target_encoded = urllib.parse.quote_plus(target)
        url = f"https://wttr.in/{target_encoded}?format=3"
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        weather_text = resp.text.strip()
        # Some responses include extra newline or information; keep it concise:
        if weather_text:
            print(weather_text)
            speak(weather_text)
            return weather_text
        else:
            msg = "Sorry, I couldn't fetch the weather right now."
            print(msg)
            speak(msg)
            return msg
    except requests.RequestException:
        msg = "Sorry, I'm unable to contact the weather service right now."
        print(msg)
        speak(msg)
        return msg
    
# Main execution loop
# --- Integrate into main loop ---

while True:
    command = listen_for_command()
    if "open" in command:
        open_application(command)
    elif "weather" in command:
        # Try to extract city after words like "in" or "for"
        city = None
        words = command.split()
        if " in " in command:
            # simple extraction: everything after " in "
            city = command.split(" in ", 1)[1].strip()
        elif " for " in command:
            city = command.split(" for ", 1)[1].strip()
        get_weather(city)
    elif "exit" in command:
        speak("Goodbye.")
        break
