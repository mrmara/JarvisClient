import random, string
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os
import logging
from include.config import logLevel
from include.utils import srcPath

class MQTTclient():
    # Define ENDPOINT, CLIENT_ID_BASE, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT
    ENDPOINT = "a33k3qhzx4b7nb-ats.iot.us-east-1.amazonaws.com"
    PATH_TO_CERT = "cert/jarvis_client.cert.pem"
    PATH_TO_KEY = "cert/jarvis_client.private.key"
    PATH_TO_ROOT = "cert/root-CA.crt"
    PORT = 443
    CLIENT_ID_BASE=''

    def __init__(self, name) -> None:
        """ 
		This method initializes aws IoT.

		This method connects to aws IoT and create a subscription for the desired topic.
		# TODO: reconnection 
		"""
        logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',level=logLevel)
        self.logger = logging.getLogger(name)
        self.name = name
        self.CLIENT_ID_BASE = name + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		# Spin up resources
        # Init AWSIoTMQTTClient
        self.myAWSIoTMQTTClient = None
        if self.PORT == 443:
            self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.CLIENT_ID_BASE, useWebsocket=True)
            self.myAWSIoTMQTTClient.configureEndpoint(self.ENDPOINT, self.PORT)
            self.myAWSIoTMQTTClient.configureCredentials(self.PATH_TO_ROOT)
        elif self.PORT == 8883:
            self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.CLIENT_ID_BASE)
            self.myAWSIoTMQTTClient.configureEndpoint(self.ENDPOINT, self.PORT)
            self.myAWSIoTMQTTClient.configureCredentials(self.PATH_TO_ROOT, self.PATH_TO_KEY, self.PATH_TO_CERT)

        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect and subscribe to AWS IoT
        if (self.myAWSIoTMQTTClient.connect()):
            self.logger.info(" Connecting to {} with client ID '{}'...".format(
                    self.ENDPOINT, self.CLIENT_ID_BASE))
            # Future.result() waits until a result is available
            self.logger.info(" Connected!")
    
    def on_message(client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    def publish(self, topic, payload, QoS=1):
        return self.myAWSIoTMQTTClient.publish(topic, payload, QoS)
    
    def subscribe(self, topic, callback, QoS=1):
        return self.myAWSIoTMQTTClient.subscribe(topic, QoS, callback)
    