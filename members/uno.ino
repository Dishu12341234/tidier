#include <SoftwareSerial.h>
#include <NewPing.h>
#include <EEPROM.h>

const byte rxPin = 10;
const byte txPin = 11;


#define TRIGGER_PIN 6  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN 7     // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 300

#define MAXHEIGHT 200  //Height of the bin

#define BIN_ID_ADDRESS 0
#define CONNECTPIN 2
#define LED 13
NewPing US(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);


SoftwareSerial NODE(rxPin, txPin);
String serverIP = "192.168.157.2";
String BinID = "#XC16s";
#define BIN_ID_LENGTH 6
unsigned long lastTimeMillis = 0;
bool allowUpdate = true;
bool loggedIn = false;

String readBinIDFromEEPROM() {
  // Read Bin ID from EEPROM
  for (int i = 0; i < 6; ++i) {  // Assuming Bin ID is 6 characters long
    BinID[i] = EEPROM.read(BIN_ID_ADDRESS + i);
  }
  BinID.trim();  // Remove any leading or trailing whitespaces
  return BinID;
}

void writeBinIDToEEPROM() {
  // Write Bin ID to EEPROM
  for (int i = 0; i < BinID.length(); ++i) {
    EEPROM.write(BIN_ID_ADDRESS + i, BinID[i]);
  }
  EEPROM.write(BIN_ID_ADDRESS + BinID.length(), '\0');  // Null-terminate the string
}

bool checkEEPROM() {
  // Check if EEPROM contains valid Bin ID
  String data = readBinIDFromEEPROM();
  for(char c : data)
  {
    if(!isAlphaNumeric(c));
  }
  return true; // EEPROM data is valid
}
void setup() {
  pinMode(CONNECTPIN, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
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
  delay(1000);
}

void connectToGetBinID() {
  String httpRequest = "                                        ";
  httpRequest += "GET /connect HTTP/1.1\r\n";
  httpRequest += "Host: " + serverIP + "\r\n";
  httpRequest += "Content-Type: application/x-www-form-urlencoded\r\n";
  String DatahttpRequest = "username=divyanshundley&password=divyansh&device=NODE";
  httpRequest += "Content-Length:" + String(DatahttpRequest.length()) + "\r\n";
  httpRequest += "\r\n";
  httpRequest += DatahttpRequest;
  httpRequest += "\n";
  httpRequest += "\r\n";

  NODE.println("AT+CIPSTART=4,\"TCP\",\"" + serverIP + "\",8000");
  delay(300);
  printResponse();
  String command = "AT+CIPSEND=4," + String(httpRequest.length() + 4);
  NODE.println(command);
  delay(100);
  NODE.print(httpRequest);
  delay(1000);
  printResponse();
}

void printResponse() {
  while (NODE.available()) {
    String data = NODE.readStringUntil('\r');
    int length = data.length();
    data.trim();
    Serial.println(data);
    if (data.indexOf("SCCS") >= 0) {
      Serial.println("Login Successful");
      loggedIn = true;
      Serial.println(US.ping_cm());
    } else if (data.indexOf("BinId") >= 0) {
      Serial.println("Got BinID");
      BinID = data.substring(6, 12);
      delay(100);
      if (BinID.length() == BIN_ID_LENGTH) {
        writeBinIDToEEPROM();
      } else {
        Serial.println("Invalid BinID received");
      }
    }
  }
}
void update() {
  String httpRequest = "                                        ";
  httpRequest += "POST /update HTTP/1.1\r\n";
  httpRequest += "Host: " + serverIP + "\r\n";
  httpRequest += "Content-Type: application/x-www-form-urlencoded\r\n";
  int fillUp = (US.ping_cm() * 100) / MAXHEIGHT;
  // fillUp = 111;
  String DatahttpRequest = "BinID=" + BinID + "&fillUp=" + String(fillUp);
  if (fillUp >= 101 || 0 >= fillUp) {  //I the percentage is >= 101 then the sensor is not in the corrct position this may be due to a refresh
    Serial.println("A value greater than 100 has been detected");
    delay(200);
    Serial.println("This maybe due to an ongoing refresh");
    delay(200);
    Serial.println("After ten seconds the system will send another update to the server if the value if in the correct limits");
    delay(200);
    Serial.println("Distance > 100 :" + String(fillUp));
    for (int i = 1; i < 10; i++) {
      Serial.print(10 - i);
      Serial.println(" seconds till update");
      digitalWrite(LED, HIGH);
      delay(500);
      digitalWrite(LED, LOW);
      delay(500);
    }
    fillUp = 0;
    update();
    return;
  }
  httpRequest += "Content-Length:" + String(DatahttpRequest.length()) + "\r\n";
  httpRequest += "\r\n";
  httpRequest += DatahttpRequest;
  httpRequest += "\n";
  httpRequest += "\r\n";

  NODE.println("AT+CIPSTART=4,\"TCP\",\"" + serverIP + "\",8000");
  delay(300);
  printResponse();
  String command = "AT+CIPSEND=4," + String(httpRequest.length() + 4);
  NODE.println(command);
  delay(100);
  NODE.print(httpRequest);
  printResponse();
}

void login() {
  if (checkEEPROM()) {
    BinID = readBinIDFromEEPROM();
  }
  String httpRequest = "                                        ";
  httpRequest += "POST /loginUser HTTP/1.1\r\n";
  httpRequest += "Host: " + serverIP + "\r\n";
  httpRequest += "Content-Type: application/x-www-form-urlencoded\r\n";
  String DatahttpRequest = "username=divyanshundley&password=divyansh&device=NODE";
  httpRequest += "Content-Length:" + String(DatahttpRequest.length()) + "\r\n";
  httpRequest += "\r\n";
  httpRequest += DatahttpRequest;
  httpRequest += "\n";
  httpRequest += "\r\n";

  NODE.println("AT+CIPSTART=4,\"TCP\",\"" + serverIP + "\",8000");
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
    } else if (loggedIn && digitalRead(CONNECTPIN)) {
      digitalWrite(CONNECTPIN, HIGH);
      delay(300);
      digitalWrite(CONNECTPIN, LOW);
      delay(300);
      connectToGetBinID();
    } else if (loggedIn && allowUpdate) {
      update();
    } else {
      Serial.println("Failed to login");
    }
    lastTimeMillis = millis();
  }
}