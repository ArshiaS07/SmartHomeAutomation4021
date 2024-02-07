import speech_recognition as sr
import random
import os
import time
from playsound import playsound
from connect import *
from IPs import *

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
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        print("Error; {0}".format(e))
    return text

def process_voice_command(text):
    actions = {
        "open door": "d1",
        "close door": "d0",
        "open water": "w1",
        "close water": "w0",
        "open gas": "g1",
        "close gas": "g0",
        "light on": "l1",
        "light off": "l0",
        "play music": "music",
        "stop music" : "stop"
    }
    for command, action in actions.items():
        if all(word in text.lower() for word in command.split()):
            return action

    print("I didn't understand that command. Please try again.")
    return None
"""
def main():
    while True:
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        end_program = process_voice_command(text)
        if end_program is not None:
            break

    if end_program == "l1":
        thread = threading.Thread(target=send_data , args = (1 , IP["light"]))
        thread.start()
    if end_program == "l0":
        thread = threading.Thread(target=send_data , args = (0 , IP["light"]))
        thread.start()
    if end_program == "w1":
        thread = threading.Thread(target=send_data , args = (1 , IP["water"]))
        thread.start()
    if end_program == "w0":
        thread = threading.Thread(target=send_data , args = (0 , IP["water"]))
        thread.start()
    if end_program == "g1":
        thread = threading.Thread(target=send_data , args = (1 , IP["gas"]))
        thread.start()
    if end_program == "g0":
        thread = threading.Thread(target=send_data , args = (0 , IP["gas"]))
        thread.start()
    if end_program == "d1":
        thread = threading.Thread(target=send_data , args = (1 , IP["door"]))
        thread.start()
    if end_program == "d0":
        thread = threading.Thread(target=send_data , args = (0 , IP["door"]))
        thread.start()"""
