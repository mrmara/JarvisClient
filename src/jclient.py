from src.myMqttClient import MQTTclient
from src.recognizer import recognizer
from src.speaker import speaker
from include.houndify import client_id,client_key
from include.config import logLevel
import time
import logging

class jclient():
    
    name="jarvis_kitchen"

    def __init__(self) -> None:
        logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',level=logLevel)
        self.logger = logging.getLogger(self.name)
        self.listener_engine = recognizer(name=self.name, apiType=4,client_id=client_id,client_key=client_key,language='en-EN',initActivationWordListener=False)
        self.speaker_engine = speaker()
        self.mqtt = MQTTclient(self.name)
        self.stay()

    def invoke_command(self, com):
        self.logger.debug(com)
        topic = self.name + "/request"
        self.mqtt.publish(topic, str(com), 1)
        self.logger.debug("published %s on topic %s", com, topic)
        self.mqtt.subscribe(self.name + "/response", self.say_response)
    
    def say_response(self, client, userdata, message):
        self.speaker_engine.add_to_queue(str(message.payload.decode("utf-8")))
        self.speaker_engine.speak_queue()
    
    def stay(self):
        while True:
            cmd = self.listener_engine.listen_and_recognize()
            self.invoke_command(cmd)
            time.sleep(5)