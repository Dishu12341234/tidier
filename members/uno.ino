#include <SoftwareSerial.h>
#include <NewPing.h>

const byte rxPin = 10;
const byte txPin = 11;


#define TRIGGER_PIN 6  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN 7     // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 300

#define MAXHEIGHT 200  //Height of the bin

NewPing US(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

SoftwareSerial NODE(rxPin, txPin);

unsigned long lastTimeMillis = 0;
bool loggedIn = false;
void setup() {
  Serial.begin(115200);
  NODE.begin(115200);
  NODE.println("AT+RST");
  delay(5000);
  NODE.println("AT+UART_CUR=9600,8,1,0,0");
  NODE.end();
  NODE.begin(9600);
  delay(100);
  printResponse();
  delay(1000);
  Serial.println("NODE Reset and Configured");
  NODE.println("AT+CIPMUX=1");  // Set NODE to Station mode
  delay(100);
  NODE.println("AT+CIFSR");
  printResponse();
}

void printResponse() {
  while (NODE.available()) {
    String data = NODE.readStringUntil('\n');
    delay(100);
    data.trim();
    if (data == "SCCS") {
      Serial.println("Login Successful");
      loggedIn = true;
      Serial.println(US.ping_cm());
    }
  }
}

void update() {
  String httpRequest = "                                        ";
  httpRequest += "POST /update HTTP/1.1\r\n";
  httpRequest += "Host: 192.168.157.2\r\n";
  httpRequest += "Content-Type: application/x-www-form-urlencoded\r\n";
  int fillUp = (US.ping_cm() * 100) / MAXHEIGHT;
  String DatahttpRequest = "BinID=#XC16&fillUp=" + String(fillUp);
  if (fillUp > 100 || 0 >= fillUp) {
    Serial.println("A refresh has been detected");
    Serial.println("The system will delay for 10 seconds ");
    Serial.println("After the delay the values will be sent to the server");
    for (int i = 1; i < 10; i++) {
      Serial.print(10-i);
      Serial.println(" seconds till update");
      delay(1000);
    }
  }
  httpRequest += "Content-Length:" + String(DatahttpRequest.length()) + "\r\n";
  httpRequest += "\r\n";
  httpRequest += DatahttpRequest;
  httpRequest += "\n";
  httpRequest += "\r\n";

  NODE.println("AT+CIPSTART=4,\"TCP\",\"192.168.157.2\",8000");
  delay(300);
  printResponse();
  String command = "AT+CIPSEND=4," + String(httpRequest.length() + 4);
  NODE.println(command);
  delay(100);
  NODE.print(httpRequest);
  delay(1000);
  printResponse();
}

void login() {
  String httpRequest = "                                        ";
  httpRequest += "POST /loginUser HTTP/1.1\r\n";
  httpRequest += "Host: 192.168.157.2\r\n";
  httpRequest += "Content-Type: application/x-www-form-urlencoded\r\n";
  String DatahttpRequest = "username=divyanshundley&password=divyansh&device=NODE";
  httpRequest += "Content-Length:" + String(DatahttpRequest.length()) + "\r\n";
  httpRequest += "\r\n";
  httpRequest += DatahttpRequest;
  httpRequest += "\n";
  httpRequest += "\r\n";

  NODE.println("AT+CIPSTART=4,\"TCP\",\"192.168.157.2\",8000");
  delay(300);
  printResponse();
  String command = "AT+CIPSEND=4," + String(httpRequest.length() + 4);
  NODE.println(command);
  delay(100);
  NODE.print(httpRequest);
  delay(1000);
  printResponse();
}

void loop() {
  if (millis() - lastTimeMillis > 1000) {
    if (!loggedIn) {
      login();
    } else {
      update();
    }
    lastTimeMillis = millis();
    return;
  }

  if (NODE.available()) {
    Serial.write(NODE.read());
  }
}