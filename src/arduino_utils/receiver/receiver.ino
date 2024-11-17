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

IRrecvPCI myReceiver(2); // pin number for the receiver
IRsendRaw mySender;
bool communication_started = false;
uint16_t command[700];
int read_index = 0;
void setup()
{
  Serial.begin(115200);
  myReceiver.enableIRIn(); // Start the receiver
  Serial.println(F("Ready to receive IR signals"));
}

void loop()
{
  static long unsigned beginRecv;
  if (read_index != 0 && !communication_started){
    Serial.println("Sending command");
    mySender.send(command,read_index,36);
    delay(1000);
  }
  else if (myReceiver.getResults())
  {
    if (!communication_started)
    {
      communication_started = true;
      Serial.println(F("Communication started"));
      beginRecv = millis();
    }
    for (bufIndex_t i = 1; i < recvGlobal.recvLength; i++)
    {
      Serial.print(recvGlobal.recvBuffer[i], DEC);
      command[read_index] = recvGlobal.recvBuffer[i];
      if (read_index < 700)
      {
        read_index++;
      }
      else
      {
        Serial.println("Buffer overflow");
      }
      if (i < recvGlobal.recvLength - 1)
      {
        Serial.print(F(", "));
      }
    }
    myReceiver.enableIRIn(); // Restart receiver
  }
  else if (communication_started && (millis() - beginRecv > 1500))
  {
    if (communication_started)
    {
      Serial.println();
      Serial.print("Communication ended after ");
      Serial.print((millis() - beginRecv) / 1000.0);
      Serial.println(" seconds");
      communication_started = false;
    }
  }
  myReceiver.enableIRIn(); // Restart receiver
}
