#define _DEBUG_
#define _DISABLE_TLS_
#define THINGER_USE_STATIC_MEMORY
#define THINGER_STATIC_MEMORY_SIZE 512 // we define static memory of thinger
#include <WiFi.h> // include library for wifi connexion
#include <ThingerWifi.h> // include library for web interface connexion
#define USERNAME "Amos" // web interface username
#define DEVICE_ID "Amosmuteb" //  device ID wich we go throu the web
#define DEVICE_CREDENTIAL "nxtbC9y9t55n" // credential passeword
#define SSID "HUAWEI P20 Amos" // wifi name throu we are online
#define SSID_PASSWORD "impossible351" //connexion password
ThingerWifi thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL); // information wich is use for to establish the link
#include "Wire.h" // 
#include <Sparkfun_APDS9301_Library.h> // light sensor library
APDS9301 apds;
#define INT_PIN 6// We'll connect the INT pin from our sensor to the 
bool lightIntHappened = false; // flag set in the interrupt to let the
#define  A0;

// testing sketch for various DHT humidity/temperature sensors
#include "DHT.h"
#define DHTPIN 9     // Digital pin connected to the DHT sensor
// Feather HUZZAH ESP8266 note: use pins 3, 4, 5, 12, 13 or 14 --
// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);
int val = 0;
float t;
float h;
float f;

void setup() {
  thing.add_wifi(SSID, SSID_PASSWORD); // configure wifi network
  Serial.begin(9600); // define serial port for communication
  pinMode(LED_BUILTIN, OUTPUT);
  thing["led"] << digitalPin(LED_BUILTIN); // pin control example (i.e. turning on/off a light, a relay, etc)
  delay(5);    // The CCS811 wants a brief delay after startup.
  
  Wire.begin();
  apds.begin(0x39);  // We're assuming you haven't changed the I2C address from the default by soldering the jumper on the back of the board.
  apds.setGain(APDS9301::LOW_GAIN); // Set the gain to low. Strictly speaking, this isn't necessary, as the gain defaults to low.
  apds.setIntegrationTime(APDS9301::INT_TIME_13_7_MS); // Set the integration time to the shortest interval. Again, not strictly necessary, as this is
  apds.setLowThreshold(0); // Sets the low threshold to 0, effectively disabling the low side interrupt.
  apds.setHighThreshold(50); // Sets the high threshold to 500. This is an arbitrary number I pulled out of thin 
  //  air for purposes of the example. When the CH0 reading exceeds this level, an interrupt will be issued on the INT pin.
  apds.setCyclesForInterrupt(1); // A single reading in the threshold range will cause an interrupt to trigger.
  apds.enableInterrupt(APDS9301::INT_ON); // Enable the interrupt.
  apds.clearIntFlag();  // Interrupt setup
  pinMode(INT_PIN, INPUT_PULLUP); // This pin must be a pullup or have a pullup resistor on it as the interrupt is a   
  attachInterrupt(digitalPinToInterrupt(INT_PIN), lightInt, FALLING);
  Serial.println(apds.getLowThreshold());
  Serial.println(apds.getHighThreshold());
  Serial.println(F("Capteur DHT11 !")); // print the text in the bracket
  dht.begin(); //
  pinMode(0, INPUT);
  
  thing["lux"] >> outputValue(apds.readCH0Level());
  thing["Température"] >> outputValue(t);
  thing["Humidité_ambiante"] >> outputValue(h);
  thing["Humidite_du_sol"] >> outputValue(val);


}
void loop() {
  thing.handle();
  Serial.println("TEST"); // print the text on the bracket on the screen when the program goes on
  static unsigned long outLoopTimer = 0;
  apds.clearIntFlag();   //  the current lux reading.
  if (millis() - outLoopTimer >= 1000) // This is a once-per-second timer that calculates and prints off
  {
    outLoopTimer = millis();
    Serial.print("Luminous flux: "); // analog read
    Serial.println(apds.readCH0Level(), 6); // print the value of the sensor on the screen
    if (lightIntHappened)
    {
      Serial.println("Interrupt"); 
      lightIntHappened = false; // state of the interrupt
    }
  }
    
  delay(2000); // Wait a few seconds between measurements.
  
  pinMode(6, OUTPUT); // sets the digital pin 3 as output
  val = analogRead(0); //connect sensor to Analog 0
  Serial.println(val);//print the value to serial port
  delay(100); // waits for a second

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  h = dht.readHumidity(); // Read temperature as Celsius (the default)
  t = dht.readTemperature(); // Read temperature as Fahrenheit (isFahrenheit = true)
  f = dht.readTemperature(true); // Check if any reads failed and exit early (to try again).
  
  if(isnan(h) || isnan(t) || isnan(f)){
    Serial.println(F("Failed to read from DHT sensor!")); // at least what the program will do if the sensor doesn't work
    return;
  }
  float hif = dht.computeHeatIndex(f, h); // Compute heat index in Fahrenheit (the default)
  float hic = dht.computeHeatIndex(t, h, false); // Compute heat index in Celsius (isFahreheit = false)
  Serial.print(F("Humidity: ")); //print the text in the bracket on the monitor
  Serial.print(h); // print the value of the humidity on the monitor
  Serial.print(F("%  Temperature: ")); //print the text in the bracket on the monitor
  Serial.print(t);// print the value of the temperature on the monitor
  Serial.print(F("°C ")); //print the text in the bracket on the monitor
  Serial.print(f);// print the value of the celcius value on the monitor
  Serial.print(F("°F  Heat index: ")); //print the text in the bracket on the monitor
  Serial.print(hic);// print the value of the fareinet value on the monitor
  Serial.print(F("°C ")); //print the text in the bracket on the monitor
  Serial.print(hif);// print the value of the humidity on the monitor
  Serial.println(F("°F")); //print the text in the bracket on the monitor
  
  if (h < 30 || t > 30) {   // if h < 30% or t > 30 °C blink red LED
    pinMode(9, OUTPUT);    // sets the digital pin 3 as output
    digitalWrite(9, HIGH); // sets the digital pin 3 on
    delay(200);            // waits for a second
    digitalWrite(9, LOW);  // sets the digital pin 3 off
    delay(200);            // waits for a second
    return;
  }
  else if (val > 480) {
    pinMode(2, OUTPUT);    // sets the digital pin 3 as output
    pinMode(3, OUTPUT);    // sets the digital pin 4 as output
    digitalWrite(2, HIGH); // sets the digital pin 3 on
    digitalWrite(3, HIGH); // sets the digital pin 4 on
    return;
  }
  else {
    pinMode(4, OUTPUT); // sets the digital pin 5 as output
    digitalWrite(4, HIGH); // sets the digital pin 5 on
    return;
  }

}
  
void lightInt()
{
  lightIntHappened = true; 
}