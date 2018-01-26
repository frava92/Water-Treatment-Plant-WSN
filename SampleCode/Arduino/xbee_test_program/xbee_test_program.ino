#include <XBee.h>
#include <Wire.h>

#define DIR_central_node 0x0C01
#define address 97
//Creating the Xbee object
XBee xbee = XBee();
unsigned long start = millis();

//allocate 20 bytes for to hold reading from DO
uint8_t payload[20] = {0};

// 16-bit addressing: Enter address of remote XBee, typically the coordinator
Tx16Request tx = Tx16Request(DIR_central_node, payload, sizeof(payload));

//Receive reponses to TX_DATA from central node
TxStatusResponse txStatus = TxStatusResponse();

//Xbee Receive Config
XBeeResponse response = XBeeResponse();

// create reusable response objects for responses we expect to handle
Rx16Response rx16 = Rx16Response();



int statusLed = 11;
int errorLed = 12;
int dataLed = 10;
int testLed = 13;

uint8_t option = 0;
uint8_t PCRequest = 0;
uint8_t rssi = 0;

char DO_data[20];       //Data from the DO (reading, information or status)
char ODRequest[20];     //Request sent to the DO (read, info, status, sleep)
byte responseCode = 0;  //Used to hold the response code coming from the DO (Success, Failed, Pending, No Data)
byte incomingTX = 0;    //Used as a buffer for the incoming data from the DO

void flashLed(int pin, int times, int wait) {

    for (int i = 0; i < times; i++) {
      digitalWrite(pin, HIGH);
      delay(wait);
      digitalWrite(pin, LOW);

      if (i + 1 < times) {
        delay(wait);
      }
    }
}


void setup() {
  pinMode(statusLed, OUTPUT);
  pinMode(errorLed, OUTPUT);
  pinMode(dataLed,  OUTPUT);
  pinMode(testLed,  OUTPUT);
  //Start serial comm
  Serial.begin(9600);
  xbee.setSerial(Serial);
  Wire.begin();
}

void loop() {
  xbee.readPacket();
  byte i = 0;                   //counter used for DO_data array.
  if (xbee.getResponse().isAvailable()) {
    //got something
    if (xbee.getResponse().getApiId() == RX_16_RESPONSE) {
      //got a rx packet
      xbee.getResponse().getRx16Response(rx16);
      option = rx16.getOption();
      rssi = rx16.getRssi();
      PCRequest = rx16.getData(0);
      if (PCRequest == 0x52) {
        //Request Reading
        strcpy(ODRequest, "r");
        digitalWrite(testLed, HIGH);
        delay(2000);
        digitalWrite(testLed, LOW);
      } else if (PCRequest == 0x49){
        //Request Info
        strcpy(ODRequest, "i");
      } else if (PCRequest == 0x53) {
        //Request Status
        strcpy(ODRequest, "status");
      } else if (PCRequest == 0x5A) {
        //Sleep
        strcpy(ODRequest, "sleep");
      }
      Wire.beginTransmission(address);
      Wire.write(ODRequest);
      Wire.endTransmission();
      digitalWrite(testLed, HIGH);
      delay(2000);
      digitalWrite(testLed, LOW);

      Wire.requestFrom(address, 20, 1); //call the circuit and request 20 bytes (this may be more than we need)
      responseCode = Wire.read();               //the first byte is the response code, we read this separately.

      switch (responseCode) {                   //switch case based on what the response code is.
        case 1:                         //decimal 1.
          Serial.println("Success");    //means the command was successful.
          break;                        //exits the switch case.

        case 2:                         //decimal 2.
          Serial.println("Failed");     //means the command has failed.
          break;                        //exits the switch case.

        case 254:                      //decimal 254.
          Serial.println("Pending");   //means the command has not yet been finished calculating.
          break;                       //exits the switch case.

        case 255:                      //decimal 255.
          Serial.println("No Data");   //means there is no further data to send.
          break;                       //exits the switch case.
      }

      while (Wire.available()) {       //are there bytes to receive.
        incomingTX = Wire.read();         //receive a byte.
        DO_data[i] = incomingTX;          //load this byte into our array.
        i += 1;                        //incur the counter for the array element.
        if (incomingTX == 0) {            //if we see that we have been sent a null command.
          i = 0;                       //reset the counter i to 0.
          Wire.endTransmission();      //end the I2C data transmission.
          break;                       //exit the while loop.
        }
      }
      /*for (int j = 0; j <=20; j++) {
        payload[j] =  uint8_t(DO_data[j]);
      }*/
      memcpy(payload, DO_data, 20);
      xbee.send(tx);



    }
    else {
        //not something we were expecting
        flashLed(errorLed, 1, 25);
      }
  } else if (xbee.getResponse().isError()) {
      flashLed(errorLed, 1, 25);
  }
}
