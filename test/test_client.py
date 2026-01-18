import sys, random, string
from pathlib import Path
workspace_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(workspace_root))
from mqtt_client import mqtt_client


def say_response(client, userdata, message):
    print(f"\nresponse is {str(message.payload.decode('utf-8'))}\n")
    
if __name__ == "__main__":
    mqtt = mqtt_client.MQTTClient("test_client", "jarvis_kitchen")
    while True:
        input_str = input("Enter message to send: ")
        payload: dict = {"command": input_str}
        unique_effimeral_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        mqtt.publish_request_async("", payload, say_response, id=unique_effimeral_ID)
    
