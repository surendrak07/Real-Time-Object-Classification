#include <Servo.h>

// Base servo
Servo baseServo;
const int baseServoPin = 9;
int baseAngle = 0;  // Starting angle for the base servo

// Gripper servo
Servo gripperServo;
const int gripperServoPin = 10;
const int gripperOpenAngle = 190;
const int gripperCloseAngle = 155;

void setup() {
  baseServo.attach(baseServoPin);
  gripperServo.attach(gripperServoPin);
  Serial.begin(9600);
  gripperServo.write(gripperOpenAngle);
  baseServo.write(baseAngle);
  Serial.println("Enter base angle:");
}

void loop() {
  if (Serial.available() > 0) {
    int inputAngle = Serial.parseInt();
    if (inputAngle >= 0 && inputAngle <= 180) { 
      baseAngle = inputAngle;
      delay(2000);
      gripperServo.write(gripperCloseAngle);
      for (int angle = 0; angle <= baseAngle; angle++) {
        baseServo.write(angle);
        delay(25); 
      }
      gripperServo.write(gripperOpenAngle);
      delay(750);
      baseServo.write(baseAngle);
    } 
  }
}
