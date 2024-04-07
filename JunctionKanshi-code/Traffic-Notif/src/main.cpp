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

String trafficStatus;
String timeTraffic = "09:10 AM";
String dateTraffic = "08/04/2024";
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
	lcd.print(dateTraffic);
	lcd.setCursor(0,3);
	lcd.print("Time: ");
	lcd.print(timeTraffic);
	Serial.println("LCD updated");
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
        // setLED();
    }
	   setLCD();
	//    delay(10000); //change for 1 minute = 60000
}

void initLCD(){
	Wire.begin(SDA, SCL);
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
//   Serial.begin(9600); 
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
