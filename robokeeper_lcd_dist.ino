//Include the LiquidCrystal header file which is inside the Arduino IDE
#include <LiquidCrystal.h> 

/* ==== PINS ASSIGNMNET ==========
 * LCD RS pin to digital pin 8
 * LCD EN pin to digital pin 9
 * LCD D4 pin to digital pin 4
 * LCD D5 pin to digital pin 5
 * LCD D6 pin to digital pin 6
 * LCD D7 pin to digital pin 7
 * Backlight PWM control to Pin 10
 * LCD R/W pin to ground
*/

// Set the I/O pin for LCD 4-bit mode following the library assignment: 
//  LiquidCrystal(rs, en, d4, d5, d6, d7).
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

int analogPin = A0;  //Define the A0 as analogPin as integer type.
int adc_key_old;
int adc_key_in;
int NUM_KEYS = 5;
int key=-1;
int adc_key_val[5] ={30, 150, 360, 535, 760 }; //Define the value at A0 pin 
                                               // when a key is pressed.
                    
                    
// The setup() method runs once, when the sketch starts
void setup ()
{
  Serial.begin(9600); // open a serial connection to display values
  lcd.begin(16, 2);            // set the lcd type: 16-character by 2-lines
  //lcd.clear();                        // LCD screen clear
  lcd.print("Hi");      // Send the ASCII code to the LCD for 
                                      // displaying the message

  // pinMode(10, OUTPUT);                // sets backlight pin-10 as PWM output
  // analogWrite(10, 125);               // Set backlight to 50% brightness 
    
  // lcd.setCursor(0,1);           // set the position of next message string: 
                                // 1st position at 2nd line
  
}

void loop()
{
  if (Serial.available()) {
    // wait a bit for the entire message to arrive
    delay(100);
    // clear the screen
    lcd.clear();
    // read all the available characters
    while (Serial.available() > 0) {
      // display each character to the LCD
      lcd.write(Serial.read());
    }
  }
}
