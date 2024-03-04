#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define MQTT_BROKER       "broker.hivemq.com"
#define MQTT_PORT         1883
#define HIVEMQ_USERNAME   "taist_aiot_dev"
#define MQTT_NOTIFICATION  "taist/aiot/notification/dev_00"

#define WIFI_SSID         "wifi_username"
#define WIFI_PASSWORD     "wifi_password"


const int LED_GREEN_PIN = 46; // green button
const int LED_YELLOW_PIN = 45; // yellow button
const int LED_RED_PIN = 21; // red button
String trafficStatus = "high"; // traffic status

WiFiClient wifi_client;
PubSubClient mqtt_client(wifi_client);

// Function to set the LEDs based on traffic status
void setLED() {
  if (trafficStatus == "high") {
    digitalWrite(LED_RED_PIN, HIGH);
    digitalWrite(LED_GREEN_PIN, LOW);
  } else if (trafficStatus == "low") {
    digitalWrite(LED_RED_PIN, LOW);
    digitalWrite(LED_GREEN_PIN, HIGH);
  } else {
    digitalWrite(LED_RED_PIN, LOW);
    digitalWrite(LED_GREEN_PIN, LOW);
  }
}

void setup(){
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_YELLOW_PIN, OUTPUT);
  pinMode(LED_RED_PIN, OUTPUT);
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
    }


void loop() {
  setLED();
  delay(1000); // Wait for 1 second
  // getStatus()
  Serial.println("OK");
}

