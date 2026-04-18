#include <Adafruit_NeoPixel.h>

// Pin Definitions
const int sensorPin = A0;
const int neoPixelPin = 6;  // The pin connected to WS2812 DIN

// LED Array Setup
const int numPixels = 8;    // Number of LEDs on your WS2812 stick
Adafruit_NeoPixel strip(numPixels, neoPixelPin, NEO_GRB + NEO_KHZ800);

// Calibration Values 
// IMPORTANT: Update these based on your specific sensor!
const int valueInDryAir = 1023; 
const int valueInWater = 300;   

void setup() {
  Serial.begin(9600);
  
  // Initialize the WS2812 array
  strip.begin();           
  strip.show();            // Initialize all pixels to 'off'
  strip.setBrightness(50); // Set brightness to ~20% (0-255 scale) to save power
}

void loop() {
  int rawSensorValue = analogRead(sensorPin);
  
  // Convert raw reading to a 0-100 percentage
  int moisturePercent = map(rawSensorValue, valueInDryAir, valueInWater, 0, 100);
  moisturePercent = constrain(moisturePercent, 0, 100);
  
  Serial.print("Soil Moisture: ");
  Serial.print(moisturePercent);
  Serial.println("%");

  // Determine the color based on moisture levels
  uint32_t statusColor;
  
  if (moisturePercent <= 70) {
    statusColor = strip.Color(255, 0, 0); // Red
  } 
  else if (moisturePercent > 70 && moisturePercent <= 90) {
    statusColor = strip.Color(255, 255, 0); // Yellow
  } 
  else {
    statusColor = strip.Color(0, 255, 0); // Green
  }

  // Apply the color to all 8 LEDs simultaneously
  strip.fill(statusColor, 0, numPixels);
  strip.show(); // Send the updated data to the LEDs

  delay(500); // Wait half a second before taking the next reading
}
