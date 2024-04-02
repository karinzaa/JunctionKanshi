import paho.mqtt.client as mqtt
import json
import time
import sys

# MQTT broker configuration
mqtt_broker_address = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic = "taist/aiot/junctionkanshi/camera1"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}, {userdata}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        print(f"Received message on topic {msg.topic}: {data}")
        if int(data['vehicleCount'])>20:
            traffic_status = "HIGH"
            print(traffic_status)
        
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_address, mqtt_port)

try:
    while True:
        client.loop_start()  # Start networking daemon
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    print("Exiting...")
    client.disconnect()