#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Queue.h>

#define MQTT_BROKER       "broker.hivemq.com"
#define MQTT_PORT         1883
#define HIVEMQ_USERNAME   "taist_aiot_dev"
#define MQTT_TOPIC  "taist/aiot/junctionkanshi/camera1/status"

#define WIFI_SSID         "wifi_username"
#define WIFI_PASSWORD     "wifi_password"

String trafficStatus;     

const int LED_GREEN_PIN = 46;
const int LED_YELLOW_PIN = 45;
const int LED_RED_PIN = 21;

WiFiClient wifi_client;
PubSubClient mqtt_client(wifi_client);

// queue handle
// QueueHandle_t evt_queue;

// Function to set the LEDs based on traffic status
void setLED() {
  if (trafficStatus == "HIGH") {
    digitalWrite(LED_RED_PIN, HIGH);
    digitalWrite(LED_GREEN_PIN, LOW);
  } 
  else if (trafficStatus == "LOW") {
    digitalWrite(LED_RED_PIN, LOW);
    digitalWrite(LED_GREEN_PIN, HIGH);
  } 
  Serial.println("LED state updated");
}

// callback function when command is received
void on_cmd_received(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received on topic: ");
  Serial.println(topic);
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
    message.remove(0, 1);  // Remove the first quote
    message.remove(message.length() - 1);  // Remove the last quote

    Serial.print("Message received: ");
    Serial.println(message);
    if (message != trafficStatus) {
        trafficStatus = message;
        setLED();
    }
}

// task to received the message
void comm_task(){
  // initialize the network
  Serial.begin(115200);
  WiFi.mode(WIFI_OFF);
  delay(100);
  WiFi.mode(WIFI_STA);
  delay(100);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  mqtt_client.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt_client.setCallback(on_cmd_received);
  mqtt_client.connect(HIVEMQ_USERNAME);

  mqtt_client.subscribe(MQTT_TOPIC);
}

void setup(){
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_YELLOW_PIN, OUTPUT);
  pinMode(LED_RED_PIN, OUTPUT);
  comm_task();
}

void loop() {
  if (mqtt_client.connected()) {
    mqtt_client.loop();
    Serial.println("MQTT loop");
  }
   else {
    Serial.println("MQTT disconnected");
  }
  delay(1000);
}

