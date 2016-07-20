/* Raw IR commander
 
 This sketch/program uses the Arduno and a PNA4602 to 
 decode IR received.  It then attempts to match it to a previously
 recorded IR signal
 
 Code is public domain, check out www.ladyada.net and adafruit.com
 for more tutorials! 
 */

// We need to use the 'raw' pin reading methods
// because timing is very important here and the digitalRead()
// procedure is slower!
//uint8_t IRpin = 2;
// Digital pin #2 is the same as Pin D2 see
// http://arduino.cc/en/Hacking/PinMapping168 for the 'raw' pin mapping
#define IRpin_PIN      PIND
#define IRpin          2

// the maximum pulse we'll listen for - 65 milliseconds is a long time
#define MAXPULSE 65000
#define NUMPULSES 160

// what our timing resolution should be, larger is better
// as its more 'precise' - but too large and you wont get
// accurate timing
#define RESOLUTION 20 

// What percent we will allow in variation to match the same code
#define FUZZINESS 20


#define ONE_ON_TIME 60
#define ONE_OFF_TIME 115

#define ZERO_ON_TIME 60
#define ZERO_OFF_TIME 35

// we will store up to 100 pulse pairs (this is -a lot-)
uint16_t pulses[NUMPULSES][2];  // pair is high and low pulse 
uint8_t currentpulse = 0; // index for pulses we're storing

//#include "ircodes.h"

void setup(void) {
  Serial.begin(9600);
  Serial.println("Ready to decode IR!");
}

void loop(void) {
  int numberpulses;
  
  numberpulses = listenForIR();
  
  Serial.print("Heard ");
  Serial.print(numberpulses);
  Serial.println("-pulse long IR signal");
  char readFromIR = IRConvertToBinary(numberpulses);
  Serial.println(readFromIR);
  //if (IRcompare(numberpulses, ApplePlaySignal,sizeof(ApplePlaySignal)/4)) {
  //  Serial.println("PLAY");
  //}
  //  if (IRcompare(numberpulses, AppleRewindSignal,sizeof(AppleRewindSignal)/4)) {
  //  Serial.println("REWIND");
  //}
  //  if (IRcompare(numberpulses, AppleForwardSignal,sizeof(AppleForwardSignal)/4)) {
  //  Serial.println("FORWARD");
  //}
  delay(500);
}

// #define DEBUG_TWO
// #define DEBUG_ONE
// #define DEBUG_THREE

boolean isAOne(int oncode, int offcode) {

    #ifdef DEBUG_THREE
      printCodes(oncode, offcode, "?");
    #endif
    
    // check to make sure the error is less than FUZZINESS percent
    int comparisonOn = abs(oncode - ONE_ON_TIME);
    int fuzzyPercentageOn = (ONE_ON_TIME * FUZZINESS / 100);
    #ifdef DEBUG_THREE
      Serial.print("comparisonOn was: ");
      Serial.print(comparisonOn);
      Serial.print(", ");
      Serial.print("percMatchOn was: ");
      Serial.println(fuzzyPercentage);
    #endif

    int comparisonOff = abs(offcode - ONE_OFF_TIME);
    int fuzzyPercentageOff = (ONE_OFF_TIME * FUZZINESS / 100);
    #ifdef DEBUG_THREE
      Serial.print("comparisonOff was: ");
      Serial.print(comparisonOff);
      Serial.print(", ");
      Serial.print("percMatchOff was: ");
      Serial.println(fuzzyPercentageOff);
    #endif
    
    if ( comparisonOn > fuzzyPercentageOn ) {
      // we didn't match perfectly, return a false match
      return false;
    }

     if ( comparisonOff > fuzzyPercentageOff ) {
      // we didn't match perfectly, return a false match
      return false;
    }
    return true;
}


boolean isAZero(int oncode, int offcode) {
    // check to make sure the error is less than FUZZINESS percent
    if ( abs(oncode - ZERO_ON_TIME) > (ZERO_ON_TIME * FUZZINESS / 100)) {
      // we didn't match perfectly, return a false match
      return false;
    }

     if ( abs(offcode - ZERO_OFF_TIME) > (ZERO_OFF_TIME * FUZZINESS / 100)) {
      // we didn't match perfectly, return a false match
      return false;
    }
    return true;
}    

void printCodes(int oncode, int offcode, char* digitVal) {
    Serial.print("oncode: ");
    Serial.print(oncode);
    Serial.print(", ");
    Serial.print("offcode: ");
    Serial.print(offcode);
    Serial.print(", ");
    Serial.print("digit: ");
    Serial.println(digitVal);
}

#define FORCE_MESSAGE_LENGTH_ONE_CHAR

char IRConvertToBinary(int count){
#ifdef FORCE_MESSAGE_LENGTH_ONE_CHAR
  count = 8;
#endif
  unsigned char output = 0;
  unsigned char message[(count/8) +1];

  memcpy( message, 0, (count/8)+1);
  int index = 0;
  for( int _bit=0; _bit < count; _bit++)
  {
    //for 8 bits

      // current bit on
      int oncode = pulses[_bit][1] * RESOLUTION / 10;
  
      // current bit off
      int offcode = pulses[_bit+1][0] * RESOLUTION / 10;
      
      if( isAOne(oncode,offcode) ) {
        output |= 1 << (7-(_bit%8));
        #ifdef DEBUG_ONE
          printCodes(oncode ,offcode, "1");
        #endif
      } else if ( isAZero(oncode, offcode) ) {
        //seems important, but not sure what todo
        ;
        #ifdef DEBUG_ONE
          printCodes(oncode, offcode, "0");   
        #endif
      } 
      //printCodes(oncode, offcode, ".");
  
    if ( _bit % 8 == 0 ){
       //then you have a character ready to do something with
       message[index] = output;
       index++;
      //Serial.print("<");
      Serial.write(output);
      //Serial.print(">");
      output = 0; 
    }
  }
  Serial.println("");
 // Everything matched!
 return output;
}

//KGO: added size of compare sample. Only compare the minimum of the two
boolean IRcompare(int numpulses, int Signal[], int refsize) {
  int count = min(numpulses,refsize);
  Serial.print("count set to: ");
  Serial.println(count);
  for (int i=0; i< count-1; i++) {
    int oncode = pulses[i][1] * RESOLUTION / 10;
    int offcode = pulses[i+1][0] * RESOLUTION / 10;
    
#ifdef DEBUG    
    Serial.print(oncode); // the ON signal we heard
    Serial.print(" - ");
    Serial.print(Signal[i*2 + 0]); // the ON signal we want 
#endif   
    
    // check to make sure the error is less than FUZZINESS percent
    if ( abs(oncode - Signal[i*2 + 0]) <= (Signal[i*2 + 0] * FUZZINESS / 100)) {
#ifdef DEBUG
      Serial.print(" (ok)");
#endif
    } else {
#ifdef DEBUG
      Serial.print(" (x)");
#endif
      // we didn't match perfectly, return a false match
      return false;
    }
    
    
#ifdef DEBUG
    Serial.print("  \t"); // tab
    Serial.print(offcode); // the OFF signal we heard
    Serial.print(" - ");
    Serial.print(Signal[i*2 + 1]); // the OFF signal we want 
#endif    
    
    if ( abs(offcode - Signal[i*2 + 1]) <= (Signal[i*2 + 1] * FUZZINESS / 100)) {
#ifdef DEBUG
      Serial.print(" (ok)");
#endif
    } else {
#ifdef DEBUG
      Serial.print(" (x)");
#endif
      // we didn't match perfectly, return a false match
      return false;
    }
    
#ifdef DEBUG
    Serial.println();
#endif
  }
  // Everything matched!
  return true;
}

int listenForIR(void) {
  currentpulse = 0;
  
  while (1) {
    uint16_t highpulse, lowpulse;  // temporary storage timing
    highpulse = lowpulse = 0; // start out with no pulse length
  
//  while (digitalRead(IRpin)) { // this is too slow!
    while (IRpin_PIN & (1 << IRpin)) {
       // pin is still HIGH

       // count off another few microseconds
       highpulse++;
       delayMicroseconds(RESOLUTION);

       // If the pulse is too long, we 'timed out' - either nothing
       // was received or the code is finished, so print what
       // we've grabbed so far, and then reset
       
       // KGO: Added check for end of receive buffer
       if (((highpulse >= MAXPULSE) && (currentpulse != 0))|| currentpulse == NUMPULSES) {
         return currentpulse;
       }
    }
    // we didn't time out so lets stash the reading
    pulses[currentpulse][0] = highpulse;
  
    // same as above
    while (! (IRpin_PIN & _BV(IRpin))) {
       // pin is still LOW
       lowpulse++;
       delayMicroseconds(RESOLUTION);
        // KGO: Added check for end of receive buffer
        if (((lowpulse >= MAXPULSE)  && (currentpulse != 0))|| currentpulse == NUMPULSES) {
         return currentpulse;
       }
    }
    pulses[currentpulse][1] = lowpulse;

    // we read one high-low pulse successfully, continue!
    currentpulse++;
  }
}
void printpulses(void) {
  Serial.println("\n\r\n\rReceived: \n\rOFF \tON");
  for (uint8_t i = 0; i < currentpulse; i++) {
    Serial.print(pulses[i][0] * RESOLUTION, DEC);
    Serial.print(" usec, ");
    Serial.print(pulses[i][1] * RESOLUTION, DEC);
    Serial.println(" usec");
  }
  
  // print it in a 'array' format
  Serial.println("int IRsignal[] = {");
  Serial.println("// ON, OFF (in 10's of microseconds)");
  for (uint8_t i = 0; i < currentpulse-1; i++) {
    Serial.print("\t"); // tab
    Serial.print(pulses[i][1] * RESOLUTION / 10, DEC);
    Serial.print(", ");
    Serial.print(pulses[i+1][0] * RESOLUTION / 10, DEC);
    Serial.println(",");
  }
  Serial.print("\t"); // tab
  Serial.print(pulses[currentpulse-1][1] * RESOLUTION / 10, DEC);
  Serial.print(", 0};");
}
