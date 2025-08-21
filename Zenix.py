import google.generativeai as genai # importing gemini from google.generativeai
import os # importing os for system commands
import time 
import playsound as ps # importing playsound for playing audio files
import threading # importing threading for running sound in a separate thread
import speech_recognition as sr # importing speech_recognition for voice commands
import pyttsx3 # for text-to-speech conversion
import webbrowser 

r=sr.Recognizer()

genai.configure(api_key=open("api_key.txt").read().strip())

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate',174)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def get_response_from_gemini(text):
    model= genai.GenerativeModel("gemini-2.5-flash")
    prompt=(
        'Your answer should no longer than 2 lines.'
        'You are Zinex, a personal helpful assistant.'
        'You can understand english and urdu but reply only in English'
        'You can open system apps and websites'
        'Be concise and clear in your responses.\n'
        f"User: {text}"
    )
    response= model.generate_content(prompt)
    return response.text

is_awake= True
def play_startup_sound():
    ps.playsound("Zenix_Audio.mp3")

# Start sound in a thread

sound_thread = threading.Thread(target=play_startup_sound)
sound_thread.start()
# speaks 
speak("Welcome Back Sir, I am Zinex, your Personal Artificial Intelligence Assistant. PLease wait for a moment. All systems will be prepared in few minutes.")
time.sleep(8)

while True:
    if is_awake:
       
        with sr.Microphone() as source:
            print('say something...')
            audio = r.listen(source)
        try:
            user_input= r.recognize_google(audio)
            print('You Said :', user_input)

            if "sleep" in user_input.lower() or 'sojao' in user_input.lower() or "so jao" in user_input.lower() or 'soja' in user_input.lower() or 'so ja' in user_input.lower():
                is_awake = False
                speak("Going to Sleep...")
                continue
            elif 'exit' in user_input.lower():
                speak("Good bye! See you soon.")
                break
            elif "open google" in user_input.lower() or 'google open' in user_input.lower():
                speak("Opening Google")
                webbrowser.open("https://www.google.com")
                continue               
            elif 'open youtube' in user_input.lower() or 'youtube open' in user_input.lower():
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")
                continue
            elif "open lms" in user_input.lower() or "lms open" in user_input.lower() or "lm open" in user_input.lower() or "open lm" in user_input.lower():  
                speak("Opening AIOU LMS.")
                webbrowser.open("https://aaghi.aiou.edu.pk/")
                continue
            elif "open google" and "search" in user_input.lower() or "google open" and "search" in user_input.lower():
                query = user_input[17:].strip()
                if query:
                    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    speak(f"Searching Google for {query}")
                    webbrowser.open(url)
                    continue
            elif "open google" in user_input.lower() or "google open" in user_input.lower():
                    speak("Opening Google")
                    webbrowser.open("https://www.google.com")
                    continue
            elif "open cm" in user_input.lower() or 'cm open' in user_input.lower() or 'cm open' in user_input.lower() or ' open cms' in user_input.lower():
                speak ("opening AIOU CMS")
                webbrowser.open("https://cms.aiou.edu.pk/")
                continue
            elif "portfolio" in user_input.lower():
                speak("Opening your portfolio.")
                webbrowser.open("https://masahir.site")
                continue
            elif "shutdown" in user_input.lower() or "shut down" in user_input.lower() or 'laptop off' in user_input.lower():
                speak("Shutting down the system.")
                os.system("shutdown /s /t 1")
                break
            elif "open whatsapp" in user_input.lower() or "whatsapp open" in user_input.lower():
                os.system("start whatsapp://")
            elif "open MS word" in user_input.lower() or "MS word open" in user_input.lower():
                os.system("start winword")
            elif "open excel" in  user_input.lower() or "excel open" in user_input.lower():
                os.system("start excel")
            elif "open powerpoint" in  user_input.lower() or "powerpoint open" in user_input.lower():
                os.system("start powerpnt")
            elif"open notepad" in user_input.lower() or "notepad open" in user_input.lower():
                os.system("start notepad")
            elif"open settings" in user_input.lower() or "settings open" in user_input.lower():
                os.system("start ms-settings:")
            elif"open calculator" in  user_input.lower() or "calculator open" in  user_input.lower() :
                os.system("start calc")
            elif"open linkedin" in  user_input.lower() or "linkedin open" in user_input.lower():
                os.system("start https://www.linkedin.com")
            elif "what time is it" in user_input.lower() or "time" in user_input.lower():
                clock_time=time.strftime("%I %M:%p")
                speak(f'The current time is {clock_time}')
                print(f'The current time is {clock_time}')
                continue
            
            reply = get_response_from_gemini(user_input)
            print("zinex", reply)
            speak(reply)
            
        except Exception:
            speak("Sorry I could not understand")
        time.sleep(0.5)
    else:
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            user_input = r.recognize_google(audio)
            if 'awake' in user_input.lower() or 'jag jao' in user_input.lower() or "wakeup" in user_input.lower() or 'wake up' in user_input.lower() or "jagjao" in user_input.lower() or "jaag jao" in user_input.lower() or "jaagjao" in user_input.lower():
                is_awake = True
                speak("Okay, I'm listening")
        except Exception:
            pass