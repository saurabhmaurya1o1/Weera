#include <Servo.h>

Servo servoPan;  // X-axis
Servo servoTilt; // Y-axis

const int panPin = 9;   // Connect Pan servo signal here
const int tiltPin = 10; // Connect Tilt servo signal here
const int relayPin = 8; // Connect Relay control here

// Relay Logic (Change these if your relay behaves backwards)
const int RELAY_ON = LOW;  
const int RELAY_OFF = HIGH; 

void setup() {
  Serial.begin(9600);
  
  // Attach servos
  servoPan.attach(panPin);
  servoTilt.attach(tiltPin);
  
  // Initialize Relay
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, RELAY_OFF); // Ensure pump is OFF on startup
  
  // Move to default center position
  servoPan.write(90);
  servoTilt.write(90);
  delay(1000);
}

void loop() {
  // Check if Python sent data
  if (Serial.available() > 0) {
    // Look for the start marker '<'
    if (Serial.read() == '<') {
      
      // Parse the comma-separated integers
      int targetX = Serial.parseInt();
      int targetY = Serial.parseInt();
      int triggerSpray = Serial.parseInt();
      
      // Look for the end marker '>'
      if (Serial.read() == '>') {
        
        // 1. Move Servos
        servoPan.write(targetX);
        servoTilt.write(targetY);
        
        // Wait a fraction of a second for mechanical movement to finish
        delay(300); 
        
        // 2. Trigger Pump if requested
        if (triggerSpray == 1) {
          digitalWrite(relayPin, RELAY_ON);
          delay(1000); // SPRAY FOR 1 SECOND
          digitalWrite(relayPin, RELAY_OFF);
        }
      }
    }
  }
}