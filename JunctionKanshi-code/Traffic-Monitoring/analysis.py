import paho.mqtt.client as mqtt
import json
import time
import numpy as np
import threading
from queue import Queue

class TrafficAnalyzer:
    def __init__(self, data):
        self.data = data
        self.avg_speed = 0

    def analyze_traffic(self):
        print("The number of vehicles: {}".format(self.data['vehicleCount']))
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

class MQTTClientPubSub:
    def __init__(self, broker_address, broker_port, subscribe_topic, publish_topic):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.queue = Queue()
        self.lock = threading.Lock()

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port)

    def disconnect(self):
        self.client.disconnect()

    def subscribe(self):
        self.client.subscribe(self.subscribe_topic)

    def on_message(self, client, userdata, message):
        payload = json.loads(message.payload.decode('utf-8'))
        with self.lock:
            self.queue.put(payload)

    def publish_json(self, data):
        payload = json.dumps(data)
        self.client.publish(self.publish_topic, payload)
        print("Published:", payload)

    def run(self):
        self.connect()
        self.subscribe()
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def publish_loop(self):
        while True:
            if not self.queue.empty():
                with self.lock:
                    data = self.queue.get()
                    traffic_analyzer = TrafficAnalyzer(data)
                    traffic_analyzer.analyze_traffic()
                    traffic_status = traffic_analyzer.get_traffic_status()    
                    data = {'traffic_status': traffic_status,
                            'datetime': data['datetime']}
                    print("Publishing data...")
                    self.publish_json(data)

if __name__ == "__main__":
    # MQTT broker configuration
    mqtt_broker_address = "broker.hivemq.com"
    mqtt_port = 1883
    mqtt_topic_subscribe = "taist/aiot/junctionkanshi/camera1/detection"
    mqtt_topic_publish = "taist/aiot/junctionkanshi/camera1/status"

    client = MQTTClientPubSub(mqtt_broker_address, mqtt_port, mqtt_topic_subscribe, mqtt_topic_publish)
    client_thread = threading.Thread(target=client.run)
    publish_thread = threading.Thread(target=client.publish_loop)

    client_thread.daemon = True
    publish_thread.daemon = True

    client_thread.start()
    publish_thread.start()

    print("MQTT client is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Stopping MQTT client...")
        client.disconnect()
        print("MQTT client stopped.")