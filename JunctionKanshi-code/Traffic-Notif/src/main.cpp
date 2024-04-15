#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
// #include <Queue.h>

#define MQTT_BROKER       "broker.hivemq.com"
#define MQTT_PORT         1883
#define HIVEMQ_USERNAME   "taist_aiot_dev"
#define MQTT_TOPIC  	  "taist/aiot/junctionkanshi/camera1/status"

#define WIFI_SSID         "wifi_username"
#define WIFI_PASSWORD     "wifi_password"

String trafficStatus, dateStr, timeStr;
LiquidCrystal_I2C lcd(0x27, 20, 04);
     

// const int LED_GREEN_PIN = 15;
// const int LED_YELLOW_PIN = 2;
// const int LED_RED_PIN = 4;

WiFiClient wifi_client;
PubSubClient mqtt_client(wifi_client);

// queue handle
// QueueHandle_t evt_queue;

// Function to set the LEDs based on traffic status
// void setLED() {
//   if (trafficStatus == "HIGH") {
//     digitalWrite(LED_RED_PIN, HIGH);
//     digitalWrite(LED_GREEN_PIN, LOW);
//   } 
//   else if (trafficStatus == "LOW") {
//     digitalWrite(LED_RED_PIN, LOW);
//     digitalWrite(LED_GREEN_PIN, HIGH);
//   } 
//   Serial.println("LED state updated");
// }

void setLCD(){
	lcd.clear();
	lcd.setCursor(5,0);
	lcd.print("Traffic Jam");
	lcd.setCursor(0,1);
	lcd.print("Status: "); 
	lcd.print(trafficStatus);
	lcd.setCursor(0,2);  
	lcd.print("Date: ");
	lcd.print(dateStr);
	lcd.setCursor(0,3);
	lcd.print("Time: ");
	lcd.print(timeStr);
	Serial.println("LCD updated");
}

// callback function when command is received
void on_cmd_received(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received on topic: ");
  Serial.println(topic);
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, payload, length);

  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return;
  }

  String newTrafficStatus = doc["traffic_status"];
  const char* newDatetime = doc["datetime"];

  Serial.print("Traffic Status: ");
  Serial.println(newTrafficStatus);
  Serial.print("Datetime: ");
  Serial.println(newDatetime);

  // Separate date and time
  char date[11]; // "DD/MM/YYYY\0"
  char time[9];  // "HH:MM\0"
  strncpy(date, newDatetime, 10); // Copy first 10 characters (date) to date buffer
  date[10] = '\0'; // Null-terminate the date string
  strncpy(time, newDatetime + 11, 5); // Skip first 11 characters (date), then copy next 5 characters (time) to time buffer
  time[5] = '\0'; // Null-terminate the time string

  dateStr = date;
  timeStr = time;

  if (newTrafficStatus != trafficStatus) {
        trafficStatus = newTrafficStatus;
        // setLED();
  }
	setLCD();
	delay(10000); //change for less than 1 minute < 60000
}

void initLCD(){
	Wire.begin(SDA, SCL); //SDA=pin D21, SCL=pin D22
	lcd.begin(20,4);
	lcd.backlight();
	lcd.print("Please wait..");
	Serial.begin(9600);
}

// void initLED(){
// 	pinMode(LED_GREEN_PIN, OUTPUT);
// 	pinMode(LED_YELLOW_PIN, OUTPUT);
// 	pinMode(LED_RED_PIN, OUTPUT);
// }
// task to received the message

void comm_task(){
  // initialize the network
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
	initLCD();
	// initLED();
	comm_task();
}

void loop() {
  delay(2000);
  if (mqtt_client.connected()) {
    mqtt_client.loop();
    Serial.println("MQTT loop");
  }
   else {
    Serial.println("MQTT disconnected");
  }
  delay(1000);
}
