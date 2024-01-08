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
    if("open" in text.lower() and "door" in text.lower()) :
        return(1)
    elif("close" in text.lower() and "door" in text.lower()):
        return(0)   
    #cascacvdsvv
    elif("open" in text.lower() and "water" in text.lower()):
        return(1)
    elif("close" in text.lower() and "water" in text.lower()):
        return(0)   
    elif("open" in text.lower() and "gas" in text.lower()):
        return(1)
    elif("close" in text.lower() and "gas" in text.lower()):
        return(0)  
    elif("light" in text.lower() and "on" in text.lower()):
        return(1)
    elif("light"in text.lower() and "off" in text.lower()):
        return(0)   
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