from unicodedata import name
from src.speaker import speaker
from include.config import activation_words, timeout_activation
import speech_recognition as sr
import include.customErrors as er
import logging
import threading
import time
from src.myMqttClient import MQTTclient

class recognizer():

    def __init__(self, name, apiType: 'bing, google, google_cloud, houndify, ibm, sphinx, wit', key=None, credentials=None, language='en-US',
                    show_all=False, client_id=None, client_key=None, username ='', password='', keyword_entries=None, grammar=None, initMic = True,
                    initActivationWordListener = True) -> "Recognizer":
        super().__init__()
        self.name = name
        self.apiType = apiType
        self.engine = sr.Recognizer()
        self.key=key
        self.credentials=credentials
        self.language=language
        self.show_all=show_all
        self.client_id=client_id
        self.client_key=client_key
        self.username=username
        self.passowrd=password
        self.keyword_entries=keyword_entries
        self.grammar=grammar
        logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
        self.mqtt_client = MQTTclient(name)
        self.logger = logging.getLogger(name)
        self.speaker = speaker(welcome = False)
        self.commands_buffer=[]
        if initMic:
            self.init_microphone()
        if initActivationWordListener:
            x = threading.Thread(target=self.activation_word_listener)
            x.start()

    
    def recognize(self, audio_data) -> 'str':
        try:
            if self.apiType == 1:
                return self.engine.recognize_bing(audio_data=audio_data,key=self.key,language=self.language,show_all=self.show_all)
            elif self.apiType == 2:
                self.logger.debug("Recognizing with Google")
                return self.engine.recognize_google(audio_data=audio_data,key=self.key, language=self.language,show_all=self.show_all)
            elif self.apiType == 3:
                return self.engine.recognize_google_cloud(audio_data=audio_data, credentials_json=self.credentials, language=self.language)
            elif self.apiType == 4:
                self.logger.debug("Recognizing with Houndify")
                return self.engine.recognize_houndify(audio_data=audio_data, client_id=self.client_id, client_key=self.client_key, show_all=self.show_all)
            elif self.apiType == 5:
                return self.engine.recognize_ibm(audio_data=audio_data, username=self.username, password=self.password, language=self.language, show_all=self.how_all)
            elif self.apiType == 6:
                return self.engine.recognize_sphinx(audio_data, language=self.language, keyword_entries=self.keyword_entries, grammar=self.grammar, show_all=self.show_all)
            elif self.apiType == 7:
                return self.engine.recognize_wit(audio_data, key=self.key, show_all=False)
            else:
                raise er.RecognizerAPIError()
        except:
            return None

    def AudioFile(self, source: 'path or stream') -> 'AudioFile':
        self.audioIn = sr.AudioFile(source)
        return self.audioIn
    
    def record(self, source: 'audio file'):
        self.audioRec = self.engine.record(source)
        return self.audioRec
    
    def init_microphone(self) -> "Microphone":
        self.microphone = sr.Microphone(device_index=13)
        return self.microphone
        
    def activation_word_listener(self):
        while(True):
            rec = self.listen(timeout_activation)
            if ( rec!= None):
                recognized_rec = self.recognize(rec)
                self.logger.debug(f"last record is {recognized_rec}")
                if recognized_rec != None:
                    for word in recognized_rec.split(" "):
                        if word in activation_words:
                            self.logger.info("Jarvis is awake")
                            self.speaker.say("At your commands sir")
                            self.commands_buffer.append(self.listen_and_recognize())
            else: 
                pass
    def listen(self, timeout=10):
        self.logger.debug("I am listening")
        with self.microphone as source:
            try:
                self.engine.adjust_for_ambient_noise(source)
                self.last_rec=self.engine.listen(source, timeout=3, phrase_time_limit=timeout)
                self.logger.debug("I stopped listening")
                return self.last_rec
            except sr.WaitTimeoutError:
                self.logger.debug("sending activation rec due to timeout")
                return None

    def buffer_listening(self):
        pass
    
    def listen_and_recognize(self):
        self.logger.debug("Understanding command")
        com = self.recognize(self.listen())
        self.logger.debug(f"last command is {com}")
        if com != None:
            com = com.split(" ")
        else:
            self.listen_and_recognize()
        return com
    
    def get_last_command(self):
        if len(self.commands_buffer) > 0:
            cmd =  self.commands_buffer.pop()
        else:
            cmd = None
                   
        return cmd, len(self.commands_buffer)

