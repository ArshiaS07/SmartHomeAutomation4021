#include <WiFi.h>
#include <WebSocketsServer.h>

int Desired = 0;
#define RELAY_PIN 2
unsigned long LastTime = 0;
bool CurrentStatus = 0;

const char* ssid = "Redmi 9T";
const char* password = "12345678";
WebSocketsServer webSocket = WebSocketsServer(81);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  if (type == WStype_TEXT) {
    String receivedMessage = String((char*)payload);
    Desired = receivedMessage.toInt();
    if (Desired >= 2){
      Desired = map(Desired, 2, 100, 25, 5000);
    }
    

    Serial.println(Desired);
    
    // Serial.println("Received message: " + receivedMessage);
    // if (receivedMessage.equals("1")) {
    //   digitalWrite(ledPin, HIGH);  // Turn on the LED
    // } else if (receivedMessage.equals("0")) {
    //   digitalWrite(ledPin, LOW);  // Turn off the LED
    // }
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
  pinMode(RELAY_PIN, OUTPUT_OPEN_DRAIN); // Set the LED pin as output
}
// int time1, time2; 
 void loop() {
  webSocket.loop();
  if (Desired == 1 || Desired == 0) {
    digitalWrite(RELAY_PIN, Desired == 1 ? LOW : HIGH); // Set pin HIGH for 1 and LOW for 0
  }

  if (Desired >= 2) {
    if (millis() - LastTime > Desired) {
      digitalWrite(RELAY_PIN, CurrentStatus ? HIGH : LOW);
      CurrentStatus = !CurrentStatus;
      LastTime = millis();
    }
  }
    //Serial.println("Flashing Mode");
  // time2 = millis();
  // Serial.println(time2-time1);


}  // put your main code here, to run repeatedly:
