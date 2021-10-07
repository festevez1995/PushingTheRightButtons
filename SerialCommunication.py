## @file SerialCommunication.py
#  Brief doc for SerialCommunication.py
#
#  Detailed doc for SerialCommunication.py
#  The main program for Lab 3.
#  This is the front end user interface
#  This utilizes the serial communication
#
#  @author Fernando Estevez
#
#  @copyright License Info
#
#  @date January 31, 2021

import serial
import keyboard
import struct
import numpy
import matplotlib.pyplot as plt 

## Set up serial communication
#
#  Sets up a serial communication with the Nucleo Board.
#  Port = COM3 baudrate = 115000 timeout = 1
#  @return ser Returns a Serial Object
def setupSerialCom():
    # Creats a serial Object
    ser = serial.Serial(port='COM3',baudrate=115000,timeout=1)
    return ser

## Send Char
#
#  Sends an Ascii character to the Nucleo board
#  @param ser Serial Object
def sendChar(ser):
    inv = "g"
    ser.write(str(inv).encode('ascii'))
    myval = ser.readline().decode('ascii')
    return myval

## Converts a digital Voltage to its analog Voltage
#
#  @param digitalValue The digital value from the ADC
def convertADC(digtalValue):
    # Voltage 
    Vref = 3.3
    # ADC Resolution
    res = 4095
    # Equation to convert digital voltage to its analog voltage
    return ((Vref / res) * digtalValue)

## The begining of the Serial Interface
#
#  UI front-end which runs on your PC and receives user input.
#  If the user presses ‘G,’the Nucleo™ should await a button press. 
#  When data collection is complete, the script should generate both a plot 
#  of voltage vs. time and a .CSV file of data. 
#  Note that the plot should include labeled axes with appropriate units.
#
def main():
    # Sets up a serial com Object
    serialCom = setupSerialCom()
    voltage_list = []
    print("Welcome!")
    print("To quit press CTR + C")
    print("Press g to begin serial communication: ")
    # Wait for input intil Pressed Ctr + C
    while True:

        try:
            # If G is pressed, Nucleo will wait for button pressed 
            if keyboard.is_pressed('g'):
                print("Press the button:")
                # Send the ascii value of the press
                serialCom.write(str("g").encode('ascii'))
                
                # wait until data has been writen
                while True:
                    if serialCom.inWaiting() > 0:
                        break
                
                # once we have serial data read the first 4 bytes
                out = serialCom.read(4)
                idx = 0
                # repeat until all the data has been writen
                while idx < 500:
                    # convert our bytearray value to an int
                    out_array = struct.unpack('<HH', out)
                    # add our final value to our voltage array
                    voltage_list.append(convertADC(out_array[0]))
                    voltage_list.append(convertADC(out_array[1]))
                    # grab the next 4 bytes of data
                    out = serialCom.read(4)
                    idx +=1
                # Creats a time array
                time_array = []
                time = 0
                # since we are running at a freqency of 200KHz our period is
                # 5us. We will be stepping through each ADC Value by 5 us
                for i in range(len(voltage_list)):
                    time_array.append(time)
                    time += .000005
                    
                # Plots our data
                plt.plot(time_array, voltage_list)
                # Gives appropriate labels to our plot
                plt.xlabel('Time')
                plt.ylabel('Voltage')
                plt.title('ADC: Voltage vs. Time')
                # Coonverts my 2 arrays into a 2x1000 array
                CSVOut = numpy.column_stack((voltage_list, time_array ))
                # writes our new 2d array to a csv file
                numpy.savetxt("ADCData.csv", 
                              CSVOut, delimiter=",", 
                              header='Voltage,Time')

                break
            else:
                pass
                
        except KeyboardInterrupt:
            keyboard.unhook_all()
            break
    
    print("Good bye!")
    serialCom.close()

    

if __name__ == "__main__":
    main()
