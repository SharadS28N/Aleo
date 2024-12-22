import speech_recognition as sr
import google.generativeai as genai
import webbrowser
import pyttsx3
import time
import requests
from datetime import datetime
from langdetect import detect
import yt_dlp
import vlc
from config import gemini_api_key, weather_api_key

# Global variables
stop_flag = False
current_player = None
music_playing = False

# Configure Google Gemini API
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
convo = model.start_chat(history=[])

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Function to select female voice (if available)
def set_voice(lang="en"):
    global voices
    for voice in voices:
        if lang in voice.languages and "female" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            print(f"Selected voice: {voice.name}")
            break
    else:
        # If no female voice is found, set to the first available voice
        engine.setProperty('voice', voices[1].id)
        print(f"Default voice: {voices[1].name}")

# Utility Functions
def get_response(user_input):
    convo_message = convo.send_message(user_input)
    print(f"[DEBUG] Gemini Response: {convo_message.text}")
    return convo_message.text

def speak(text, lang='en'):
    if lang == 'ne':
        engine.setProperty('voice', 'nepali_voice_id')  # Replace with actual Nepali voice ID if supported
    else:
        engine.setProperty('voice', engine.getProperty('voices')[0].id)
    engine.say(text)
    engine.runAndWait()

def play_music(song_name):
    global current_player, music_playing, stop_flag
    try:
        ydl_opts = {'format': 'bestaudio/best', 'noplaylist': True, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
            url = info['url']
            title = info['title']
            speak(f"Playing {title} from YouTube.")
            
            if current_player is not None:
                current_player.stop()
            
            current_player = vlc.MediaPlayer(url)
            current_player.play()
            music_playing = True

            duration = info.get('duration', 0)
            elapsed = 0
            while elapsed < duration:
                if stop_flag:
                    current_player.stop()
                    music_playing = False
                    speak("Music stopped.")
                    return
                time.sleep(1)
                elapsed += 1
            current_player.stop()
            music_playing = False
    except Exception as e:
        speak(f"Error playing music: {str(e)}")
        current_player = None

def stop_music():
    global current_player, music_playing
    if current_player is not None:
        try:
            current_player.stop()
            music_playing = False
            speak("Music stopped.")
        except Exception as e:
            print(f"[ERROR] Failed to stop music: {str(e)}")
    else:
        speak("No music is currently playing.")

def set_alarm(time_str):
    try:
        alarm_time = datetime.strptime(time_str, "%H:%M").time()
        speak(f"Alarm set for {alarm_time.strftime('%H:%M')}.")
        while True:
            if datetime.now().time() >= alarm_time or stop_flag:
                if stop_flag:
                    speak("Alarm stopped.")
                    return
                speak("Time to wake up!")
                break
            time.sleep(1)
    except ValueError:
        speak("Please provide the time in HH:MM format.")

def get_weather(city):
    try:
        city = city.strip().replace(" ", "+")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url).json()
        
        if response.get("cod") == 200:
            weather = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            city_name = response["name"]
            speak(f"The weather in {city_name} is {weather} with a temperature of {temp} degrees Celsius.")
        else:
            error_message = response.get("message", "Unknown error")
            speak(f"City not found or error occurred: {error_message}.")
    except Exception as e:
        speak(f"Error fetching weather: {str(e)}")

# Main loop
wake_word = ["hello","elio", "helio", "aleo", "a.leo", "alio", "ayleeo","aeleeo", "e.li.o", "alleo", "ayleo", "alieo", "A.L.U", "L.eo","Hi","Hello", "A.Leeyo","Aaleo","wake"]
exit_commands = ["exit", "stop", "quit", "bye"]
stop_commands = ["aleo stop", "stop aleo"]

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
current_player
def handle_commands():
    global stop_flag
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening for command...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"User: {command}")

                if any(stop_cmd in command for stop_cmd in stop_commands):
                    stop_flag = True
                    speak("Stopping assistant.")
                    break

                # Special Case for "Who made you?"
                if "who made you" in command or "who created you" in command:
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
                    if "weather" in command:
                        city = command.replace("weather in", "").strip()
                        get_weather(city)
                    elif command.startswith("play "):
                        song_name = command.replace("play ", "").strip()
                        play_music(song_name)
                    else:
                        response = get_response(command)
                        speak(response)
            except sr.UnknownValueError:
                speak("Sorry, I didn't understand that.")
            except Exception as e:
                speak(f"An error occurred: {str(e)}")

# Auto-start and main loop
if __name__ == "__main__":
    try:
        speak("Starting Aleo...")
        while True:
            if stop_flag:
                print("[DEBUG] Assistant stopped.")
                break
            command = listen_for_wake_word()
            if any(word in command for word in wake_word):
                speak("Yes, how can I assist?")
                handle_commands()
    except Exception as e:
        print(f"[DEBUG] Unexpected Error: {str(e)}")
