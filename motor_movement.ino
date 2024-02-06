
#include <Stepper.h>

// Number of steps per output rotation
const int stepsPerRevolution = 200;

// Create Instance of Stepper library
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

// Current position (measured from origin)
double current = 182; // !!! remeasure width to make sure values are correct 

// Boundaries of the linear gantry
double MAX = 182; //!!! what is the max positive x-coord (ask enrique)
double MIN = -182;

// Calibration:
double STEPS = 1218; // # steps to move across table
double length = 364; // this is in mm (can convert to 36.4 based on Enrique's code)

// New position to move to (measured from origin)
double goal = 0;

void setup() {
  // set the speed at 300 rpm:
  myStepper.setSpeed(300);
  // initialize the serial port:
  Serial.begin(9600);
  
}

void loop() {
  if (Serial.available() > 0){

    double goal = Serial.readStringUntil('\n').toDouble();

    Serial.print("RECIEVED: ");
    Serial.println(goal);
    
    // Net distance to move 
    double dist = abs(current-goal);

    if (MIN <= goal && goal <= MAX){
      if (current < goal){
        myStepper.step(-(dist*(double(STEPS)/length))); // !!!want to remeasure width
        current += dist;
      } else if (current > goal){
        myStepper.step((dist*(double(STEPS)/length)));
        current -= dist;
      } else {
        myStepper.step(0);
      }
    }
  }
}
