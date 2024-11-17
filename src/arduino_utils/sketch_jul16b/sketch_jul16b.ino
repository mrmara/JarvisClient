/* rawSend.ino Example sketch for IRLib2
 *  Illustrates how to send a code Using raw timings which were captured
 *  from the "rawRecv.ino" sample sketch.  Load that sketch and
 *  capture the values. They will print in the serial monitor. Then you
 *  cut and paste that output into the appropriate section below.
 */
#include <IRLibSendBase.h>    //We need the base code
#include <IRLib_HashRaw.h>    //Only use raw sender
#include <IRLibRecvPCI.h> 
#define dht_apin A0 // Analog Pin sensor is connected to

IRrecvPCI myReceiver(2);//pin number for the receiver
IRsendRaw mySender;
bool ok = true;
void setup() {
  Serial.begin(115200);
  myReceiver.enableIRIn(); // Start the receiver
  Serial.println(F("Ready to receive IR signals"));
  myReceiver.setFrameTimeout(100000);
}
/* Cut and paste the output from "rawRecv.ino" below here. It will 
 * consist of a #define RAW_DATA_LEN statement and an array definition
 * beginning with "uint16_t rawData[RAW_DATA_LEN]= {…" and concludes
 * with "…,1000};"
 */
#define RAW_DATA_LEN 212
uint16_t rawDataOff[RAW_DATA_LEN]={
  3722, 1938, 406, 538, 406, 1478, 406, 534, 
  410, 1474, 410, 534, 406, 1478, 406, 538, 
  406, 1474, 410, 534, 410, 1474, 406, 538, 
  406, 1474, 410, 1474, 410, 534, 406, 1478, 
  406, 538, 406, 1474, 410, 1474, 406, 1478, 
  410, 1474, 406, 538, 406, 534, 406, 1478, 
  406, 1478, 406, 534, 410, 534, 410, 534, 
  406, 538, 406, 1478, 406, 538, 406, 534, 
  406, 538, 406, 538, 406, 534, 410, 534, 
  406, 538, 406, 538, 406, 534, 410, 534, 
  406, 538, 406, 1474, 410, 538, 406, 534, 
  410, 534, 406, 1478, 406, 538, 406, 534, 
  406, 538, 406, 1478, 406, 1478, 406, 534, 
  410, 534, 410, 534, 406, 1478, 406, 534, 
  410, 534, 410, 534, 406, 538, 406, 1474, 
  410, 534, 410, 1474, 406, 538, 406, 538, 
  406, 534, 410, 534, 406, 538, 406, 1478, 
  406, 1478, 406, 1474, 410, 1474, 406, 538, 
  406, 538, 406, 538, 406, 534, 406, 538, 
  406, 534, 410, 534, 410, 534, 406, 534, 
  410, 1478, 406, 534, 410, 534, 410, 534, 
  406, 538, 406, 534, 410, 534, 406, 538, 
  406, 534, 410, 534, 410, 534, 410, 1474, 
  406, 538, 406, 1478, 406, 1474, 410, 1474, 
  406, 1478, 406, 1478, 406, 538, 406, 538, 
  406, 534, 406, 538, 406, 538, 406, 1474, 
  410, 534, 406, 1000};

#define RAW_DATA_LEN 212
uint16_t rawDataOn[RAW_DATA_LEN]={
  3722, 1938, 410, 534, 406, 1474, 410, 534, 
  410, 1474, 406, 534, 410, 1474, 410, 534, 
  410, 1474, 406, 538, 406, 1478, 406, 534, 
  410, 1474, 410, 1474, 406, 538, 406, 1474, 
  410, 534, 410, 1474, 406, 1474, 410, 1478, 
  406, 1474, 410, 534, 410, 534, 406, 1478, 
  406, 1474, 410, 534, 410, 534, 410, 534, 
  406, 534, 410, 1474, 410, 534, 406, 534, 
  410, 538, 406, 534, 410, 534, 406, 534, 
  410, 538, 406, 534, 406, 538, 406, 538, 
  406, 538, 406, 1474, 410, 534, 410, 534, 
  406, 534, 410, 534, 410, 1474, 410, 534, 
  406, 534, 410, 1474, 410, 1474, 410, 534, 
  406, 534, 410, 538, 406, 1474, 410, 534, 
  410, 534, 406, 1474, 410, 1474, 410, 534, 
  410, 534, 406, 1478, 406, 534, 410, 534, 
  406, 538, 410, 534, 406, 534, 410, 1474, 
  410, 1474, 406, 1478, 406, 1474, 410, 534, 
  410, 534, 410, 534, 406, 538, 406, 534, 
  410, 534, 410, 534, 406, 534, 410, 538, 
  406, 1474, 410, 534, 406, 538, 406, 534, 
  410, 534, 410, 534, 410, 534, 406, 538, 
  406, 534, 410, 534, 406, 538, 406, 1474, 
  410, 534, 410, 1474, 410, 1474, 406, 1478, 
  406, 1474, 410, 1478, 406, 534, 410, 534, 
  406, 538, 406, 534, 410, 534, 410, 534, 
  406, 534, 410, 1000};


/*
 * Cut-and-paste into the area above.
 */
   
void loop() {
  Serial.println("---------");
  if (ok) {
    mySender.send(rawDataOn,RAW_DATA_LEN,36);//Pass the buffer,length, optionally frequency
    Serial.println(F("AC Switched On"));
    ok = false;
  }
  else {
    mySender.send(rawDataOff,RAW_DATA_LEN,36);//Pass the buffer,length, optionally frequency
    Serial.println(F("AC Switched Off"));
    ok = true;
  }
  if (myReceiver.getResults()) { 
    Serial.println(F("Do a cut-and-paste of the following lines into the "));
    Serial.println(F("designated location in rawSend.ino"));
    Serial.print(F("\n#define RAW_DATA_LEN "));
    Serial.println(recvGlobal.recvLength,DEC);
    Serial.print(F("uint16_t rawData[RAW_DATA_LEN]={\n\t"));
    for(bufIndex_t i=1;i<recvGlobal.recvLength;i++) {
      Serial.print(recvGlobal.recvBuffer[i],DEC);
      Serial.print(F(", "));
      if( (i % 8)==0) Serial.print(F("\n\t"));
    }
    Serial.println(F("1000};"));//Add arbitrary trailing space
    myReceiver.enableIRIn();      //Restart receiver
  }
  delay(5000);
}
