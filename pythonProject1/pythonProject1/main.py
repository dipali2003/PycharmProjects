import tkinter as tk
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import datetime
import os
import smtplib
import pywhatkit
import pyjokes

recognizer = sr.Recognizer()
engine = pyttsx3.init()

root = tk.Tk()
root.title("Alexa Voice Assistant")
root.geometry("800x400")
root.configure(bg="grey")

microphone_image = tk.PhotoImage(file="microphone.png")
microphone_image = microphone_image.subsample(2, 2)

text_widget = tk.Text(root, wrap=tk.WORD, width=200, height=10, bg="white", fg="black", font=("Arial", 12))
text_widget.pack(pady=10)
text_widget.config(state=tk.DISABLED)

def respond(text):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, text)
    text_widget.config(state=tk.DISABLED)

    engine.say(text)
    engine.runAndWait()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def execute_command(command):
    if "open Google" in command:
        webbrowser.open("https://www.google.com")
    elif "open YouTube" in command:
        webbrowser.open("https://www.youtube.com")
    elif "open Wikipedia" in command:
        speak("What would you like to search on Wikipedia?")
        search_query = recognize_speech()
        if search_query:
            summary = wikipedia.summary(search_query, sentences=2)
            speak("Here is a summary from Wikipedia: " + summary)
    elif "send email" in command:
        send_email()
    elif "current time" in command:
        speak("The current time is " + get_current_time())
    elif "current date" in command:
        speak("Today is " + get_current_date())
    elif 'play' in command:
        song = command.replace('play', '')
        speak('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        speak(info)
    elif "are you single" in command:
        speak("I'm in a committed relationship with Wi-Fi!")
    elif "how are you" in command:
        speak("I'm doing fine. Thank you for asking.")
    elif 'joke' in command:
         speak(pyjokes.get_joke("tell me the joke"))
    else:
        speak("Sorry, I don't understand that command.")
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return ""
def handle_voice_command():
    respond("Yes, I'm listening. What can I do for you?")
    command = recognize_speech()
    if command:
        respond("You said: " + command)
        execute_command(command)



def get_current_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return current_date


def get_current_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return current_time



    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        print("Email could not be sent. Error:", str(e))
        speak("Sorry, I couldn't send the email.")

microphone_button = tk.Button(root, image=microphone_image, bg="blue", command=handle_voice_command, borderwidth=0)
microphone_button.place(relx=0.5, rely=0.75, anchor="center")

root.mainloop()
