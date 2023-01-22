from numpy import place
import pyttsx3
import os
from include.utils import singleton

@singleton
class speaker():

    def __init__(self, engine='espeak', welcome = True) -> None:
        self.speaker_engine = pyttsx3.init(engine)
        self.configurate()
        if welcome:
            self.welcome()

    def configurate(self) -> None:
        self.speaker_engine.setProperty("voice", 'english-us')
        self.speaker_engine.setProperty("rate", 165)
    
    def add_to_queue(self, text):
        self.speaker_engine.say(text)
    
    def speak_queue(self):
        self.speaker_engine.runAndWait()
    
    def say(self, text):
        self.speaker_engine.say(text)
        self.speak_queue()

    def welcome(self):
        self.play_sound("audio/welcome_back.mp3")

    def play_sound(self, path):
        os.system("mpg321 " + path + " >/dev/null 2>&1")
    
