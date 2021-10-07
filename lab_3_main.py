## @file lab_3_main.py
#  Brief doc for lab_3_main.py
#
#  Detailed doc for lab_3_main.py
#  The main program for Lab 3 that will be running on the nucleo board.
#  This utilizes UART
#
#  @author Fernando Estevez
#
#  @copyright License Info
#
#  @date January 31, 2021

import pyb
import array
from pyb import UART

## Checks to see if button has been pressed
buttonPressed = False


## Button interupt ISR
#
# On button pressed, set a global bool variable to True
# In order to do this, the ISR checks to see if button was poress
#
def onButtonPress(line):
    global buttonPressed
    
    if line >= 0:
        buttonPressed = True

## Main Program
#
#  The start of Lab 3 program. This will wait for a 'g' button press and 
#  return a list of ADC values to the fornt end interface
#
def main():
    # Create a UART object 
    myuart = UART(2)
    
    # Create a button object
    pinC13 = pyb.Pin(pyb.Pin.cpu.C13, mode=pyb.Pin.IN)
    binterupt = pyb.ExtInt(pinC13, 
                           mode=pyb.ExtInt.IRQ_FALLING, 
                           pull=pyb.Pin.PULL_NONE, 
                           callback=onButtonPress)

    # Ste up an ADC object
    adc = pyb.ADC(pyb.Pin.board.PC0)
    # create a timer object
    timer2 = pyb.Timer(6, freq=200000)
    # creat a buff array to hold our ADC values 
    buff = array.array('H', (0 for index in range(1000)))
    # Repeat until Nucleo button has been pressed
    while True:
        binterupt.enable()
        # Check if button was pressed
        if buttonPressed == True:
            # Only record values once we have a good ADC data
            if adc.read() > 100:
                # read adc values into a buffer with a given timer 
                adc.read_timed(buff,timer2)
                # Convert the buffer into a byte array
            
                newVolts = bytearray(buff, 'hex')
                # write the byte array back to the serial buff
                myuart.write(newVolts)
                break

if __name__ == "__main__":
    main()
