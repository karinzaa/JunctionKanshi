import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import sys

# MQTT broker configuration
mqtt_broker_address = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic_subscribe = "taist/aiot/junctionkanshi/camera1/detection"
mqtt_topic_publish = "taist/aiot/junctionkanshi/camera1/status"

# Function to publish JSON data
def publish_json(client, data):
    payload = json.dumps(data)
    client.publish(mqtt_topic_publish, payload)
    print("Published:", payload)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}, {userdata}")
    client.subscribe(mqtt_topic_subscribe)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        print(f"Received message on topic {msg.topic}: {data}")
        if int(data['vehicleCount'])>20: # temporary decision
            traffic_status = "HIGH"
        else:
            traffic_status = "LOW"
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M")    
        data = {'traffic_status': traffic_status,
                'datetime': dt_string}
        # publish traffic status data (MQTT-->the c++ file)
        publish_json(client, data)
        print(data)

        
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_address, mqtt_port)

try:
    while True:
        client.loop_start()
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    client.disconnect()

#add queue