import speech_recognition as sr
import pyttsx3
import wikipedia
import requests
import smtplib
import schedule
import time
import os
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError:
        return "Error connecting to recognition service."

def get_weather(city):
    api_key = "your_openweather_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        return f"Current temperature in {city} is {response['main']['temp']}°C."
    return "City not found."

def send_email(to_email, subject, message):
    try:
        sender_email = "your_email@gmail.com"
        sender_password = "your_email_password"
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        email_body = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to_email, email_body)
        server.quit()
        
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Failed to send email.")
        print(e)

reminders = []
def set_reminder(task, time_str):
    def reminder_job():
        speak(f"Reminder: {task}")

    schedule.every().day.at(time_str).do(reminder_job)
    reminders.append(f"{task} at {time_str}")
    speak(f"Reminder set for {task} at {time_str}")

def control_smart_home(device, action):
    speak(f"{action.capitalize()}ing {device} now.")
    print(f"{device} {action}ed successfully.")

def play_music():
    music_dir = "path_to_your_music_folder"
    songs = os.listdir(music_dir)
    if songs:
        os.system(f"start {os.path.join(music_dir, songs[0])}")
        speak("Playing music.")
    else:
        speak("No music files found.")

def main():
    speak("Hello! How can I assist you?")
    
    while True:
        command = recognize_speech()
        print(f"You said: {command}")

        if "weather" in command:
            speak("Which city?")
            city = recognize_speech()
            weather_info = get_weather(city)
            speak(weather_info)

        elif "wikipedia" in command:
            speak("What topic should I search?")
            topic = recognize_speech()
            try:
                summary = wikipedia.summary(topic, sentences=2)
                speak(summary)
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find that information.")

        elif "send email" in command:
            speak("Who should I send it to?")
            recipient = input("Enter recipient email: ")  
            speak("What is the subject?")
            subject = recognize_speech()
            speak("What is the message?")
            message = recognize_speech()
            send_email(recipient, subject, message)

        elif "set reminder" in command:
            speak("What should I remind you about?")
            task = recognize_speech()
            speak("At what time? (Format HH:MM in 24-hour format)")
            time_str = input("Enter time (HH:MM): ") 
            set_reminder(task, time_str)

        elif "control smart home" in command:
            speak("Which device?")
            device = recognize_speech()
            speak("Turn on or off?")
            action = recognize_speech()
            control_smart_home(device, action)

        elif "play music" in command:
            play_music()

        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break

        else:
            speak("I can’t perform that task yet. Try asking about weather, Wikipedia, or setting reminders.")

        schedule.run_pending() 

if __name__ == "__main__":
    main()