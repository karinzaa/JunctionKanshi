
import paho.mqtt.client as mqtt
import json
import time

# MQTT broker configuration
broker_address = "broker.hivemq.com"
broker_port = 1883
topic = "taist/aiot/junctionkanshi/traffic_status_try"  # Change this to the topic you want to publish to

# Function to publish JSON data
def publish_json(client, data):
    payload = json.dumps(data)
    client.publish(topic, payload)
    print("Published:", payload)

# Create MQTT client instance
client = mqtt.Client()

# Connect to MQTT broker
client.connect(broker_address, broker_port)

# Define JSON data to be published
data = {"vehicleCount": "10", "speed": "1.5"}
i=0
try:
    while True:
        # Publish JSON data every 1 minute
        publish_json(client, data)
        i+=1
        if i==5:
            data = {"vehicleCount": "30", "speed": "0"}
            i=0
        else:
            data = {"vehicleCount": "10", "speed": "1.5"}
        time.sleep(1)  # Wait for 1 minute
except KeyboardInterrupt:
    print("Exiting...")
    client.disconnect()