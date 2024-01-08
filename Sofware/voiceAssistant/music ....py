import speech_recognition as sr
import random, os
import time
from playsound import playsound
recognizer = sr.Recognizer()
def capture_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio
def convert_voice_to_text(audio):
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text
def process_voice_command(text):
    music_dir = r"C:\Users\Notebook\music p"
    songs = os.listdir(music_dir)
    if "music" in text.lower():
        random.shuffle(songs)  # Shuffle the list of songs
        for song in songs:
            print("Playing:", song)
            os.startfile(os.path.join(music_dir, song))
            time.sleep(1000)  # Adjust the sleep time between songs if needed

    if "hello" in text.lower():
        print("Hello! How can I help you?")
        playsound(r'C:\Users\Notebook\Downloads\quothello-therequot-158832.mp3')
    elif "bye" in text.lower():
        print("Goodbye! Have a great day!")
        playsound(r'C:\Users\Notebook\Downloads\choir-goodbyes-66120.mp3')
    
    else:
        print("I didn't understand that command. Please try again.")
    return False
def main():
    end_program = False
    while not end_program:
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        end_program = process_voice_command(text)
        

if __name__ == "__main__":
    main()
