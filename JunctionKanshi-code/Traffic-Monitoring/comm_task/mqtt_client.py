import paho.mqtt.client as mqtt
import json
import time

class MQTTClient:
    def __init__(self, broker_address, broker_port, topic):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.topic = topic
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port)

    def disconnect(self):
        self.client.disconnect()

    def publish_json(self, data):
        payload = json.dumps(data)
        self.client.publish(self.topic, payload)
        print("Published:", payload)

    def run(self, data):
        try:
            self.connect()
            self.publish_json(data)
            self.disconnect()
        except KeyboardInterrupt:
            print("Exiting...")
            self.disconnect()