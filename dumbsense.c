//+build ignore

#include <ArduinoHttpClient.h>
//#include <WiFi101.h>
#include <ESP8266WiFi.h>

#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#include <stdlib.h>

char *network = "XXXXX";
char *passwud = "YYYYY";

WiFiClient wifi;
Adafruit_BME280 bme;

void setup() {
  Serial.begin(115200);
  // Serial.setDebugOutput(true);

  bool bmestatus = bme.begin();
  if (!bmestatus) {
    Serial.println("Could not find a BME280 sensor?!");
    while (1);
  }

  Serial.println("BME280 is ready to rock.");

  Serial.print("Connecting to WiFi");
  WiFi.begin(network, passwud);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  float t = bme.readTemperature();
  float h = bme.readHumidity();
  Serial.print("Temperature = ");
  Serial.print(t);
  Serial.println("*C");
  Serial.print("Humidity = ");
  Serial.print(h);
  Serial.println("%");
  
  Serial.println("making POST request");
  char *contentType = "application/x-www-form-urlencoded";
  char buf[16];
  snprintf(buf, sizeof(buf), "t=%d&h=%d", (int)t, (int)h);

  HttpClient client = HttpClient(wifi, "dumbhome.local", 8000);
  client.post("/record", contentType, buf);
  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);

  delay(10000);
}
