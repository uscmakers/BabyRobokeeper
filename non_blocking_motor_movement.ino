#include <Arduino.h>
#include <Stepper.h>
// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200
// Target RPM for cruise speed
#define RPM 1300
// Acceleration and deceleration values are always in FULL steps / s^2
#define MOTOR_ACCEL 16000
#define MOTOR_DECEL 16000
// Microstepping mode. If you hardwired it to save pins, set to the same value here.
#define MICROSTEPS 1
#define DIR 5
#define STEP 6
#include "A4988.h"
A4988 stepper(MOTOR_STEPS, DIR, STEP);
// Current position (measured from origin)
double current = 182; // !!! remeasure width to make sure values are correct
// Boundaries of the linear gantry
double MAX = 181; //!!! what is the max positive x-coord (ask enrique)
double MIN = -181;
// Calibration:
double STEPS = 1224; // # steps to move across table
double length = 364; // this is in mm (can convert to 36.4 based on Enrique’s code)
double steps_per_mm = double(STEPS)/length;

// New position to move to (measured from origin)
double goal = 0;
// Net distance to move
double dist = 0;
unsigned wait_time_micros = 101;
int flag = 0;
void setup() {
  stepper.begin(RPM, MICROSTEPS);
  // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next line
  // stepper.setEnableActiveState(LOW);
  stepper.enable();
  stepper.setSpeedProfile(stepper.LINEAR_SPEED, MOTOR_ACCEL, MOTOR_DECEL);
  // initialize the serial port:
  Serial.begin(9600);
  delay(100);

    // set the motor to move continuously for a reasonable time to hit the stopper
    // let's say 100 complete revolutions (arbitrary number)
    stepper.startMove(1);     // in microsteps
    // stepper.startRotate(100 * 360);                     // or in degrees

    // read in initial position
    if (Serial.available() > 0){
      while (Serial.available() > 0){
        flag = 1;
        goal = Serial.readStringUntil('\n').toDouble();
      }
    }
}
void loop() {

    dist = (goal - current);
    // Serial.print("goal is "); 
    // Serial.println(goal);
    // Serial.print("current is "); 
    // Serial.println(current);
    // Serial.print("dist is "); 
    // Serial.println(dist);

    if (MIN <= goal && goal <= MAX && flag == 1){
      if (dist > 0){
        stepper.startMove(-dist*steps_per_mm); 
        // motor control loop - send pulse and return how long to wait until next pulse
        unsigned wait_time_micros = stepper.nextAction(); // how to control direction?
        current += double(length)/STEPS; 
        //Serial.println("dist pos");
      } else if (dist < 0){
        stepper.startMove(dist*steps_per_mm);  
        // motor control loop - send pulse and return how long to wait until next pulse
        // over write the start move function to move in the negative direction
        unsigned wait_time_micros = stepper.nextAction();
        current -= double(length)/STEPS;
        //Serial.println("dist neg");
      } else {
        stepper.move(0);
        //Serial.println("dist equal");
      }
    }

    if (wait_time_micros > 100){
      if (Serial.available() > 0){
        while (Serial.available() > 0){
          flag = 1;
          goal = Serial.readStringUntil('\n').toDouble();
        }
      }
    }

  }
