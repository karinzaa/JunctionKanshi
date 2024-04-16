import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import sys
import numpy as np

# MQTT broker configuration
mqtt_broker_address = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic_subscribe = "taist/aiot/junctionkanshi/camera1/detection"
mqtt_topic_publish = "taist/aiot/junctionkanshi/camera1/status"

class TrafficAnalyzer:
    def __init__(self, data):
        self.data = data
        self.avg_speed = 0

    def analyze_traffic(self):
        # Convert dictionary values to a list and convert string values to integers
        speed_values = list(self.data['speed'].values())

        # Remove 0 values from the list
        speed_values = [speed for speed in speed_values if speed != 0]

        # Check if the list is empty after removing 0 values
        if not speed_values:
            print("No non-zero speed values.")
        else:
            # Calculate mean and standard deviation
            mean_speed = np.mean(speed_values)
            std_speed = np.std(speed_values)

            # Check if the standard deviation is close to zero
            if np.isclose(std_speed, 0):
                print("Standard deviation is close to zero, cannot compute z-score.")
                print("Average speed: {} km/h".format(mean_speed))
                self.avg_speed = mean_speed
            else:
                # Calculate z-score
                z_scores = (speed_values - mean_speed) / std_speed

                # Filter elements based on condition
                filtered_speed_values = [speed_values[i] for i in range(len(speed_values)) if abs(z_scores[i]) < 1.5]

                # Check if there are filtered speed values
                if not filtered_speed_values:
                    print("No speed values with abs(z-score) < 1.5")
                else:
                    # Calculate the average of the filtered speed values
                    self.avg_speed = np.mean(filtered_speed_values)
                    print("Average of non-zero speed values with abs(z-score) < 1.5: {} km/h".format(round(self.avg_speed,2)))

    def get_traffic_status(self):
        if self.data['vehicleCount'] > 0 and self.data['vehicleCount'] <= 10 and self.avg_speed < 40:
            return "HIGH"
        else:
            return "LOW"

class Communication:
    def __init__(self, broker_address, port, subscribe_topic, publish_topic):
        self.broker_address = broker_address
        self.port = port
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.broker_address, self.port)
        self.client.loop_forever()

    def publish_json(self, data):
        payload = json.dumps(data)
        self.client.publish(self.publish_topic, payload)
        print("Published:", payload)

    def on_connect(self, client, userdata, flags, rc, properties):
        print(f"Connected with result code {rc}")
        client.subscribe(self.subscribe_topic)

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode('utf-8'))
            print(f"Received message on topic {msg.topic}: {data}")

            traffic_analyzer = TrafficAnalyzer(data)
            traffic_analyzer.analyze_traffic()
            traffic_status = traffic_analyzer.get_traffic_status()    
            data = {'traffic_status': traffic_status,
                    'datetime': data['datetime']}

            self.publish_json(data)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

communication = Communication(mqtt_broker_address, mqtt_port, mqtt_topic_subscribe, mqtt_topic_publish)
communication.connect()