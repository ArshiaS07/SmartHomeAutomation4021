#include <WiFi.h>
#include <WebSocketsServer.h>

const char* ssid = "HA";
const char* password = "12345678";
WebSocketsServer webSocket = WebSocketsServer(81);
const int ledPin = 2;

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  if (type == WStype_TEXT) {
    String receivedMessage = String((char*)payload);
    Serial.println("Received message: " + receivedMessage);
    if (receivedMessage.equals("1")) {
      digitalWrite(ledPin, HIGH);  // Turn on the LED
    } else if (receivedMessage.equals("0")) {
      digitalWrite(ledPin, LOW);  // Turn off the LED
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(10);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println(WiFi.localIP());

  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
  pinMode(ledPin, OUTPUT); // Set the LED pin as output
}

void loop() {
  webSocket.loop();
}
