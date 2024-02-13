#include <LiquidCrystal.h> // includes the LiquidCrystal Library 

LiquidCrystal lcd(5, 6, 7, 8, 9, 10);

void setup()
{
  Serial.begin(9600); // open a serial connection to display values
  lcd.begin(16, 2);
}
void loop(){
  if (Serial.available()) {
    // wait a bit for the entire message to arrive
    delay(100);
    // clear the screen
    lcd.clear();
    // read all the available characters
    lcd.write(Serial.read());
  }
}