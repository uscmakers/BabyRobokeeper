#include <Stepper.h>

// Number of steps per output rotation
const int stepsPerRevolution = 200;

// Create Instance of Stepper library
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(300);
  // initialize the serial port:
  Serial.begin(9600);
  
  // Boundaries of the linear gantry
  int MAX = 108;
  int MIN = 0;
  // Current position (measured from origin)
  int current = 0;
  // New position to move to (measured from origin)
  int update = 0;
}

void loop() {
  if (Serial.available() > 0){
    update = atoi(Serial.readStringUntil('\n'));
    
    // Net distance to move 
    int dist = abs(current-update);

    if (MIN <= update && update <= MAX){
      if (current < update){
        myStepper.step((dist/0.289));
        current += dist;
      } else if (current > update){
        myStepper.step(-(dist/0.289));
        current -= dist;
      } else {
        myStepper.step(0);
      }
    }
  }
}