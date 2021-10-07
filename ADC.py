## @file ADC.py
#  Brief doc for ADC.py
#
#  Detailed doc for ADC.py
#  Test program for ADC.
#
#  @author Fernando Estevez
#
#  @copyright License Info
#
#  @date January 31, 2021

import pyb
import utime


## Initiates Timer 2 object set to NULL.
timer2 = None
buttonPressed = False

## Function that sets up timer 2
#
# Sets up timer2 with pscale of 79 and period=0x7FFFFFFF
#
def setTimer():
    global timer2
    # Sets a larg number as the period
    p = 0x3D08FF
	# Nucleo's clock freq
    NucleoClock = 80000000
	# The freq the clock will count at - 1 MHZ
    TimerClock = 1000000
	#1Mhz clock = (80MHz/2/(prescale + 1))
    pscale = int((NucleoClock / TimerClock) - 1)
	# Sets up timer 2 object
    timer2 = pyb.Timer(2, prescaler=pscale, period=p)

def onButtonPress(line):
    global buttonPressed
    buttonPressed = True
    
## Main Program
#
#  The start of Lab 3 program
#
def main():
    print("Lab 3 begining...")
    ## Interupt pin object. Attached to C13.
    pinC13 = pyb.Pin(pyb.Pin.cpu.C13, mode=pyb.Pin.IN)
    pinC13.low()
    # Setting up an interupt
    binterupt = pyb.ExtInt(pinC13, 
                           mode=pyb.ExtInt.IRQ_FALLING, 
                           pull=pyb.Pin.PULL_NONE, 
                           callback=onButtonPress)

    # Setting up the ADC object
    adc = pyb.ADC(pyb.Pin.board.PA0)
    
    # Wait for a button press and read the adc values. 
    # then sleep for 0.1 seconds and read the next value
    while True:
        if buttonPressed == True:
            adcValue = adc.read()
            print("ADC Value: {}".format(adcValue))
            utime.sleep_ms(100)
    pass

if __name__ == "__main__":
    main()
