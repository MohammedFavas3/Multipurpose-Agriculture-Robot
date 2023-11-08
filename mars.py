#include <Servo.h>
Servo servo;
#include <HCSR04.h>
UltraSonicDistanceSensor distanceSensor(7, 8);
#include "DHT.h"
#define DHTPIN     2     // what digital pin we're connected to
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);
#include <SoftwareSerial.h>
#define rxPin 10
#define txPin 11
SoftwareSerial serial2(rxPin,txPin);

#define obj_out    A0
#define en_mot     A1
#define water       4
#define fertilizer  5
#define cuter_servo 3
#define alarm       9

unsigned long currentMillis = 0;
unsigned long previousMillis1 = 0;
unsigned int interval = 100,sec=0,msec_100=0,msec1_100=0;

unsigned int cut_en=0,dis;
long tim;
int soil_read,h,t,hic;
String data_out="#";
void timer();
void setup() 
{
 
 Serial.begin(9600);
 serial2.begin(9600);
 servo.attach(3);
 dht.begin();
 pinMode(water,OUTPUT);
 pinMode(fertilizer,OUTPUT); 
 pinMode(alarm,OUTPUT);
 pinMode(obj_out,OUTPUT);
 pinMode(en_mot,OUTPUT);
  
 digitalWrite(fertilizer,LOW);
 digitalWrite(water,LOW);

   digitalWrite(alarm,LOW);
 //****************************************  
   digitalWrite(obj_out,HIGH);
   digitalWrite(en_mot,HIGH);
 //****************************************  
 servo.write(90);
 Serial.println(" Robot starts ");
}
void cutter();
void loop() 
{
  timer();
   dis=distanceSensor.measureDistanceCm();   
   if(dis<2){dis=2;} else if(dis>100){dis=100;}
   if(dis>2 && dis<21  )
             { digitalWrite(alarm,HIGH);digitalWrite(obj_out,LOW);digitalWrite(en_mot,LOW);  }
   else if (dis>20) 
   { digitalWrite( alarm,LOW ); digitalWrite(obj_out,HIGH);digitalWrite(en_mot,HIGH);}
 
   if((millis()-tim)>3000)
    {
    h = dht.readHumidity();      
    t = dht.readTemperature();                // Read temperature as Celsius (the default)   
    tim=millis();
    }
    
  if(serial2.available()>0)
  {
   
    String rcvd = (serial2.readString().substring(0,2));
    Serial.println(rcvd);
    if ( rcvd.substring(0,1)=="*" )
    {
      if(rcvd.substring(1,2)=="C") { cut_en=1; Serial.println("cut on ");}
      if(rcvd.substring(1,2)=="c") { cut_en=0; Serial.println("cut off");}
      if(rcvd.substring(1,2)=="W") { digitalWrite(water,HIGH);Serial.println("wat on ");}
      if(rcvd.substring(1,2)=="w") { digitalWrite(water,LOW);Serial.println("wat off");}
      if(rcvd.substring(1,2)=="Z") { digitalWrite(fertilizer,HIGH);Serial.println("fer on ");}
      if(rcvd.substring(1,2)=="z") { digitalWrite(fertilizer,LOW);Serial.println("fer off");}
      if(rcvd.substring(1,2)=="N") { cut_en=1; digitalWrite(fertilizer,HIGH);digitalWrite(water,HIGH);Serial.println("auto on");}
      if(rcvd.substring(1,2)=="F") { cut_en=0; digitalWrite(fertilizer,LOW);digitalWrite(water,LOW); Serial.println("auto off"); }

    }
  }
if(cut_en==1) { cutter();}
else { servo.write(90); }
 if(sec>3){ data_out=data_out+h+t; delay(50);serial2.println(data_out);data_out="#"; sec=0; }
 //Serial.print("H:");Serial.print(h);Serial.print(" T:");Serial.print(t);Serial.print(" H:");
 //Serial.print("D:");Serial.println(dis);
 delay(100);
}
void cutter()
{
 servo.write(60); delay(100); 
 servo.write(120); delay(100);
}
void timer()
{
  currentMillis = millis();
  if ((unsigned long)(currentMillis - previousMillis1) >= interval)   // check for rollover delay 1
  {
    msec_100++;msec1_100++;
    if(msec_100>9){msec_100=0;sec++;}
    previousMillis1 = currentMillis;
  } 
}