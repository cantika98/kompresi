#include <Wire.h>
#define alamatSlave 0x04
int dataMaster = 0; //menampung data komunikasi antara master dan slave
#include "ThinkGearStreamParser.h"
#include <SoftwareSerial.h>   //Software Serial Port
#include "arduinoFFT.h"
#include <BasicLinearAlgebra.h>
#include "Toeplitz32x64.h"
#define MR 2
#define SIZE_DATA 4

double A ;
int coba;

using namespace BLA;

arduinoFFT FFT = arduinoFFT();

const uint16_t samples = SIZE_DATA; // banyak sample yang mau dipakai
int x;
double total; //bagian dari transformasi fourier
double mean; //bagian dari transformasi fourier
double vReal[samples]; //nilai real dari transformasi fourier
double vImag[samples]; //nilai imajiner dari transformasi fourier
double HvReal [samples];
double HvImag [samples];


ThinkGearStreamParser parser;

#include <SoftwareSerial.h>     // library for software serial

SoftwareSerial bluetoothSerial(2, 3);  // RX, TX komunikasi HC-05 ke arduino


void setup()
{
  Serial.begin( 9600 ); // USB serial monitor to Arduino
  bluetoothSerial.begin( 57600 ); // bluetooth serial to NeuroSky MindWave
  THINKGEAR_initParser(&parser, handleDataValueFunc, NULL); // assign the handlers for the parser
  Serial.flush();
  A = 0;
  x = 0;
  Wire.begin();
  Serial.begin(9600);

}

void loop()
{
  coba = x;
  handleDataValueFunc;
  while (!bluetoothSerial.available()) delay(4); // wait for a byte from the bluetooth connection
  THINKGEAR_parseByte(&parser, bluetoothSerial.read()); // forward the byte to the stream parser

  //FAST FOURIER TRANSFORM //

  if (coba != x) {

    if (coba < SIZE_DATA) {
      prtValue(A);
      vReal[coba] = A;
      total = total + vReal[x];
    }
    else if (coba == SIZE_DATA) {
      mean = total / SIZE_DATA;
      for (int i = 0; i < SIZE_DATA; i++) {
        vReal[i] = vReal[i] - mean;
        vImag[i] = 0;
      }
      FFT.Compute(vReal, vImag, samples, FFT_FORWARD);

      //PERKALIAN ANTARA vReal & dtoeplitz//
      int temp = 0;
      for (int j = 0; j < 2; j++) {
        for (int t = 0; t < SIZE_DATA; t++) {
          HvReal[j] = HvReal[j] + (dtoeplitz[temp] *  vReal[t]);
          HvImag[j] = HvImag[j] + (dtoeplitz[temp] *  vImag[t]);
          temp += 1;
        }
          Serial.println(HvReal[j]);
          Serial.print( "x" );
          Serial.println(HvImag[j]);
        }
      }
    }
  }
}

//HASIL SENSOR LANGSUNG TANPA ADA TRANSFORMASI ATAU RAW DATA//

void handleDataValueFunc(unsigned char extendedCodeLevel, unsigned char code, unsigned char valueLength, const unsigned char *value)
{
  if ( extendedCodeLevel == 0 )
  {

    switch ( code )
    {

      case (0x83):

        //Serial.print( "ASIC Level: " );
        //Serial.println( value[0] & 0xFF );

        A = value[0] & 0xFF;

        if ((A >= 0.5) && (A <= 2.75))
        {
          x++;
        }
        else if ((A >= 3.5) && ( A <= 6.75))
        {
          x++;
        }

        else if ((A >= 7.5 ) && (A <= 11.75))
        {
          x++;
        }

        else if ((A >= 13 ) && (A <= 29.75))
        {
          x++;
        }

        else if ((A >= 31 ) && (0x83 <= 49.75))
        {
          x++;
        }
    }
  }
}

//PEMANGGILAN RAW DATA YANG UDAH DIKELOMPOKAN//

void prtValue(double X) {
  if ((A >= 0.5) && (A <= 2.75))
  {
//    Serial.print( "Delta: " );
//    Serial.println(  X );
  }
  else if ((A >= 3.5) && ( A <= 6.75))
  {
//    Serial.print( "Thetha: " );
//    Serial.println(  X  );
  }

  else if ((A >= 7.5 ) && (A <= 11.75))
  {
//    Serial.print( "Alpha: " );
//    Serial.println(  X  );
  }

  else if ((A >= 13 ) && (A <= 29.75))
  {
//    Serial.print( "Beta: " );
//    Serial.println(  X  );
  }

  else if ((A >= 31 ) && (0x83 <= 49.75))
  {
//    Serial.print( "Gamma: " );
//    Serial.println(  X  );
  }
}
