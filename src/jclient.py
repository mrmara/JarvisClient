from enum import unique
import sys
from pathlib import Path

# Add the workspace root to Python path
workspace_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(workspace_root))

from mqtt_client import mqtt_client
from src.recognizer import recognizer
from src.speaker import speaker
from include.houndify import client_id,client_key
from include.config import logLevel
import time, threading
import logging
import random, string

class jclient():
    
    name="jarvis_kitchen"

    def __init__(self, test = False) -> None:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logLevel, datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(self.name)
        self.mqtt = mqtt_client.MQTTClient(self.name, self.name)
        self.diagnostic={"start_time":time.time()}
        self.speaker_engine = speaker(welcome=False)
        if not test:
            self.listener_engine = recognizer(name=self.name, apiType=2,client_id=client_id,client_key=client_key,language='en-EN',initActivationWordListener=True)
            # start self.stay() in a new thread
            self.t = threading.Thread(target=self.stay)
            self.t.start()
    
    def get_logger(self):
        return self.logger
    
    def invoke_command(self, com):
        '''
        Commands are sent to jarvis server for processing. Topic is:
        jarvis_kitchen/command/request
        '''
        self.logger.debug(com)
        payload: dict = {"data": com}
        unique_effimeral_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        topic = "request"
        self.mqtt.publish_request_async("", payload, self.say_response, id=unique_effimeral_ID)
    
    def say_response(self, client, userdata, message):
        self.logger.debug("response is %s",str(message.payload.decode("utf-8")))
        self.speaker_engine.add_to_queue(str(message.payload.decode("utf-8")))
        self.speaker_engine.speak_queue()
    
    def stay(self):
        while True:
            cmd, buffer_len = self.listener_engine.get_last_command()
            if cmd != None:
                self.invoke_command(cmd)
    def spin(self):
        return self.diagnostic