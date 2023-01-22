from enum import unique
from src.myMqttClient import MQTTclient
from src.recognizer import recognizer
from src.speaker import speaker
from include.houndify import client_id,client_key
from include.config import logLevel
import time
import logging
import random, string

class jclient():
    
    name="jarvis_kitchen"

    def __init__(self) -> None:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logLevel, datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(self.name)
        self.listener_engine = recognizer(name=self.name, apiType=2,client_id=client_id,client_key=client_key,language='en-EN',initActivationWordListener=True)
        self.speaker_engine = speaker(welcome=False)
        self.mqtt = MQTTclient(self.name)
        self.diagnostic={}
        self.stay()

    def invoke_command(self, com):
        self.logger.debug(com)
        unique_effimeral_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        topic = self.name + "/request/" + unique_effimeral_ID
        self.mqtt.subscribe(self.name + "/response/" + unique_effimeral_ID, self.say_response)
        self.mqtt.publish(topic, str(com), 1)
        self.logger.debug("published %s on topic %s", com, topic)
    
    def say_response(self, client, userdata, message):
        self.logger.debug("reponse is %s",str(message.payload.decode("utf-8")))
        self.speaker_engine.add_to_queue(str(message.payload.decode("utf-8")))
        self.speaker_engine.speak_queue()
    
    def stay(self):
        while True:
            cmd, buffer_len = self.listener_engine.get_last_command()
            if cmd != None:
                self.invoke_command(cmd)
    def spin(self):
        return self.diagnostic