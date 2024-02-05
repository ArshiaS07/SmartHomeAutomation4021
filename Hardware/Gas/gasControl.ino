#include <WiFi.h>
#include <WebSocketsServer.h>
#include <AccelStepper.h>


float Desired = 0;

const int STEPP_PUL = 27;
const int STEPP_DIR = 26;
const int STEPP_ENA = 25;

AccelStepper stepper (1, STEPP_PUL, STEPP_DIR);

const char* ssid = "HA";
const char* password = "12345678";
WebSocketsServer webSocket = WebSocketsServer(81);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  if (type == WStype_TEXT) {
    String receivedMessage = String((char*)payload);
    Desired = receivedMessage.toFloat();
    if (Desired > 100)
      Desired = 100;
    if (Desired < 0)
      Desired = 0;
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

  stepper.setMaxSpeed(30.0);
  stepper.setAcceleration(30.0);

}


 void loop() {

  webSocket.loop();
  stepper.run();

  stepper.moveTo(-Desired * 6);

  if(stepper.currentPosition() == stepper.targetPosition()) {
    digitalWrite(STEPP_ENA, 1);
  }
  else{
    digitalWrite(STEPP_ENA, 0);
  }

}