/*
 * Gamecube protocol implementation in an Arduino Nano with an ATmega328.
 * This was made to interface a computer's serial port with the gamecube/nintendo64
 * controller line through an arduino with an ATMega328.
 * Connect pin 2 directly to the data line (red wire on official controllers) of
 * the gamecube/n64 extension cord.
*/

/* This is the pin we will be writing to. Don't change itu nless you know what
 *  You're doing. You also need to change the ports manipulated by HC_HIGH through 
 *  DDR. See Arduino direct port manipulation for more on this.
 */

/*
 * Reset the arduino once every 49 days.
 */

#define GC_PIN 2


/* these next two macros set arduino pin 2 to input or output, which with an
 * external 1K pull-up resistor to the 3.3V rail, is like pulling it high or low.
 * These operations translate to 1 op code, which takes 2 cycles. 
 * DDR 1 means it's an output, DDR 0 means it's an input. */
// sets pin2 to input, allowing it to be pulled high, thus writing a "1" to the line
#define GC_HIGH DDRD &= 0b11111011
// sets pin2 to output, and I **THINK** this writes a "0".
#define GC_LOW DDRD |= 0b00000100  

// returns TRUE if the pin 2 is on
#define GC_QUERY (PIND & 0x04)

static byte controller_status[8];
unsigned long timestamp;

void setup(){
    /*  I'm not sure whether the output pins default to 0, so leaving this here just to make sure. */
    digitalWrite(GC_PIN, LOW);
    pinMode(GC_PIN, INPUT);
    
    Serial.begin(2000000);
    Serial.write("Hello from arduino.");
    
}

void loop(){
    while(GC_QUERY){
        // wait for GC to start asking (probably with 1 null byte.)
    }
    Serial.write('A');
    Serial.readBytes(controller_status, 8);
    while (!GC_QUERY){
        // wait for the line to go back up. (maybe we'll need to wait a little more after it comes back up, go through that stop bit)
    }
    GC_send(controller_status, 8);
    
    //debug
    Serial.write("The following will probably be fucked up. remember to copy the controllerstatus before calling gc send to see whats in there.\n");
    // Serial.write(controller_status);
}

/* This routine is very carefully timed by examining the assembly output.
Do not change any statements, it could throw the timings off. We get 16 cycles per microsecond,
which should be plenty, but we need to be conservative. Most assembly ops take 1 cycle,
but a few take 2. I use manually constructed for-loops out of gotos so I have 
more control over the outputted assembly. I can insert nops where it was impossible
with a for loop */
void GC_send(unsigned char *buffer, char length){
    // Send these bytes
    char bits;
    bool bit;
    asm volatile (";Starting outer for loop");
    outer_loop: {
        asm volatile (";Starting inner for loop");
        bits=8;
        inner_loop: {
            // Starting a bit, set the line low
            asm volatile (";Setting line to low");
            GC_LOW; // 1 op, 2 cycles

            asm volatile (";branching");
            if (*buffer >> 7) {
                asm volatile (";Bit is a 1");
                // 1 bit
                // remain low for 1us, then go high for 3us
                // nop block 1
                asm volatile ("nop\nnop\nnop\nnop\nnop\n");
                asm volatile (";Setting line to high");
                GC_HIGH;
                // nop block 2
                // we'll wait only 2us to sync up with both conditions
                // at the bottom of the if statement
                asm volatile ("nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n");
            } else {
                asm volatile (";Bit is a 0");
                // 0 bit
                // remain low for 3us, then go high for 1us
                // nop block 3
                asm volatile ("nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\nnop\n"  
                            "nop\n");
                asm volatile (";Setting line to high");
                GC_HIGH;
                // wait for 1us
                asm volatile ("; end of conditional branch, need to wait 1us more before next bit");
            }
            // end of the if, the line is high and needs to remain
            // high for exactly 16 more cycles, regardless of the previous
            // branch path
            asm volatile (";finishing inner loop body");
            --bits;
            if (bits != 0) {
                // nop block 4
                // this block is why a for loop was impossible
                asm volatile ("nop\nnop\nnop\nnop\nnop\n"  
                            "nop\nnop\nnop\nnop\n");
                // rotate bits
                asm volatile (";rotating out bits");
                *buffer <<= 1;
                goto inner_loop;
            } // fall out of inner loop
        }
        asm volatile (";continuing outer loop");
        // In this case: the inner loop exits and the outer loop iterates,
        // there are /exactly/ 16 cycles taken up by the necessary operations.
        // So no nops are needed here (that was lucky!)
        --length;
        if (length != 0) {
            ++buffer;
            goto outer_loop;
        } // fall out of outer loop
    }

    // send a single stop (1) bit
    // nop block 5
    asm volatile ("nop\nnop\nnop\nnop\n");
    GC_LOW;
    // wait 1 us, 16 cycles, then raise the line 
    // 16-2=14
    // nop block 6
    asm volatile ("nop\nnop\nnop\nnop\nnop\n"
                  "nop\nnop\nnop\nnop\nnop\n"  
                  "nop\nnop\nnop\nnop\n");
    GC_HIGH;
}

/*

void GC_get()
{
    // listen for the expected 8 bytes of data back from the controller and
    // blast it out to the N64_raw_dump array, one bit per byte for extra speed.
    // Afterwards, call translate_raw_data() to interpret the raw data and pack
    // it into the N64_status struct.
    asm volatile (";Starting to listen");
    unsigned char timeout;
    char bitcount = 32;
    char *bitbin = N64_raw_dump;

    // Again, using gotos here to make the assembly more predictable and
    // optimization easier (please don't kill me)
    read_loop:
    timeout = 0x3f;
    // wait for line to go low
    while (GC_QUERY) {
        if (!--timeout)
            return;
    }
    // wait approx 2us and poll the line
    asm volatile (
                  "nop\nnop\nnop\nnop\nnop\n"  
                  "nop\nnop\nnop\nnop\nnop\n"  
                  "nop\nnop\nnop\nnop\nnop\n"  
                  "nop\nnop\nnop\nnop\nnop\n"  
                  "nop\nnop\nnop\nnop\nnop\n"  
                  "nop\nnop\nnop\nnop\nnop\n"  
            );
    *bitbin = GC_QUERY;
    ++bitbin;
    --bitcount;
    if (bitcount == 0)
        return;

    // wait for line to go high again
    // it may already be high, so this should just drop through
    timeout = 0x3f;
    while (!GC_QUERY) {
        if (!--timeout)
            return;
    }
    goto read_loop;

}
*/ 
