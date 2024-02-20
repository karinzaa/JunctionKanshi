#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define MQTT_BROKER       "broker.hivemq.com"
#define MQTT_PORT         1883
#define HIVEMQ_USERNAME   "taist_aiot_dev"
#define MQTT_NOTIFICATION  "taist/aiot/notification/dev_00"

#define WIFI_SSID         "wifi_username"
#define WIFI_PASSWORD     "wifi_pass"

WiFiClient wifi_client;
PubSubClient mqtt_client(wifi_client);

void setup(){
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
  Serial.println("OK");
}