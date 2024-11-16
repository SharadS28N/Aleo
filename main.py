import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import webbrowser
import os
import time
import requests
from datetime import datetime
from langdetect import detect
import subprocess
import platform
from config import gemini_api_key, news_api_key, weather_api_key

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Configure Google Gemini API
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
convo = model.start_chat(history=[])

# Utility Functions
def get_response(user_input, lang='en'):
    convo_message = convo.send_message(user_input)
    return convo_message.text

def speak(text, lang='en'):
    if lang == 'ne':
        engine.setProperty('voice', 'nepali_voice_id')  # Replace with actual Nepali voice ID if supported
    else:
        engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.say(text)
    engine.runAndWait()

def detect_language(text):
    return detect(text)

def play_music(song_path):
    if os.path.isfile(song_path):
        os.system(f'start {song_path}' if os.name == 'nt' else f'open "{song_path}"')
        speak("Playing music.")
    else:
        speak("File not found.")

def set_alarm(time_str):
    try:
        alarm_time = datetime.strptime(time_str, "%H:%M").time()
        speak(f"Alarm set for {alarm_time.strftime('%H:%M')}.")
        while True:
            if datetime.now().time() >= alarm_time:
                speak("Time to wake up!")
                break
            time.sleep(1)
    except ValueError:
        speak("Please provide the time in HH:MM format.")

def set_reminder(reminder_text, reminder_time):
    try:
        reminder_time = datetime.strptime(reminder_time, "%H:%M")
        time_to_wait = (reminder_time - datetime.now()).total_seconds()
        if time_to_wait < 0:
            speak("The reminder time has already passed.")
            return
        speak(f"Reminder set for {reminder_text} at {reminder_time.strftime('%H:%M')}.")
        time.sleep(time_to_wait)
        speak(f"Reminder: {reminder_text}")
    except ValueError:
        speak("Please provide the reminder time in HH:MM format.")

def tell_joke():
    joke = "Why don't scientists trust atoms? Because they make up everything!"
    speak(joke)

def calculate(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}.")
    except Exception:
        speak("I couldn't calculate that.")

def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
        response = requests.get(url).json()
        if response["status"] == "ok":
            articles = response["articles"]
            for article in articles[:5]:
                speak(article["title"])
        else:
            speak("Unable to fetch news.")
    except Exception:
        speak("Error fetching news.")

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url).json()
        if response.get("cod") == 200:
            weather = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            speak(f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
        else:
            speak("City not found.")
    except Exception:
        speak("Error fetching weather.")

def translate_text(text, target_language):
    response = requests.post(
        'https://translate.googleapis.com/translate_a/single',
        params={'client': 'gtx', 'sl': 'auto', 'tl': target_language, 'dt': 't', 'q': text}
    )
    translated_text = response.json()[0][0][0]
    speak(translated_text)

def convert_units(amount, from_unit, to_unit):
    try:
        conversions = {
            'km_to_miles': 0.621371,
            'miles_to_km': 1.60934,
            'kg_to_pounds': 2.20462,
            'pounds_to_kg': 0.453592,
        }
        key = f"{from_unit}_to_{to_unit}"
        if key in conversions:
            result = amount * conversions[key]
            speak(f"{amount} {from_unit} is {result:.2f} {to_unit}.")
        else:
            speak("Conversion not supported.")
    except Exception:
        speak("Error in unit conversion.")

def control_volume(action):
    try:
        if os.name == 'nt':  # Windows
            if action == "up":
                os.system("nircmd.exe changesysvolume 2000")
            elif action == "down":
                os.system("nircmd.exe changesysvolume -2000")
            elif action == "mute":
                os.system("nircmd.exe mutesysvolume 1")
            elif action == "unmute":
                os.system("nircmd.exe mutesysvolume 0")
            speak(f"Volume {action}.")
    except Exception:
        speak("Error adjusting volume.")

def open_application(app_name):
    try:
        if platform.system() == "Windows":
            os.system(f'start {app_name}')
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", f"/Applications/{app_name}.app"])
        else:
            subprocess.run(["xdg-open", f"{app_name}"])
        speak(f"Opening {app_name}.")
    except Exception:
        speak("Application not found.")

def system_shutdown():
    try:
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")
        elif platform.system() == "Darwin":  # macOS
            os.system("sudo shutdown -h now")
        else:
            os.system("sudo shutdown now")
        speak("Shutting down the system.")
    except Exception:
        speak("Error shutting down the system.")

def system_restart():
    try:
        if platform.system() == "Windows":
            os.system("shutdown /r /t 1")
        elif platform.system() == "Darwin":  # macOS
            os.system("sudo shutdown -r now")
        else:
            os.system("sudo reboot")
        speak("Restarting the system.")
    except Exception:
        speak("Error restarting the system.")

# Main loop
wake_word = ["elio", "helio", "aleo", "a.leo", "hey elio", "e.li.o"]
exit_commands = ["exit", "stop", "quit", "bye"]

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for wake word...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Network error.")

def handle_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening for command...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()

                if any(word in command for word in exit_commands):
                    speak("Goodbye!")
                    break

                # Special Case for "Who made you?"
                if "who made you" in command or "who created you" in command or "who developed you" in command or "made by" in command:
                    speak("Sharad Bhandari and the Team Aleo.")
                    return

                if "news" in command:
                    get_news()
                elif "weather" in command:
                    city = command.replace("weather in", "").strip()
                    get_weather(city)
                elif "alarm" in command:
                    time_str = command.split()[-1]
                    set_alarm(time_str)
                elif "play music" in command:
                    song_path = command.replace("play music", "").strip()
                    play_music(song_path)
                elif "volume" in command:
                    action = command.split()[-1]
                    control_volume(action)
                elif "translate" in command:
                    text = command.split("translate")[-1].split("to")[0].strip()
                    target_language = command.split("to")[-1].strip()
                    translate_text(text, target_language)
                elif "open" in command:
                    app_name = command.replace("open", "").strip()
                    open_application(app_name)
                elif "shutdown" in command:
                    system_shutdown()
                elif "restart" in command:
                    system_restart()
                elif "calculate" in command:
                    expression = command.replace("calculate", "").strip()
                    calculate(expression)
                elif "reminder" in command:
                    reminder_text, reminder_time = command.replace("set reminder for", "").split(" at ")
                    set_reminder(reminder_text.strip(), reminder_time.strip())
                else:
                    language = detect_language(command)
                    response = get_response(command, language)
                    speak(response, language)

            except sr.UnknownValueError:
                speak("Sorry, I didn't understand that.")
            except sr.RequestError:
                speak("Network error.")
            except Exception as e:
                speak(f"An error occurred: {str(e)}")

# Start listening
while True:
    command = listen_for_wake_word()
    if any(word in command for word in wake_word):  # Fix here
        speak("Yes, how can I assist?")
        handle_commands()

