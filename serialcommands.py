from configurations import *
import time
import serial
import exceptions
# configure the serial connections 

class Connect(object):
    def __init__(self):

        par = PARITY
        
        if par == "none": par ="N"
        if par == "odd": par ="O"
        if par == "even": par ="E"

        # THIS NEEDS MORE WORK TO ENSURE PORT IS CONNECTED 
        try:
            self.ser = serial.Serial(
                port=PORT,
                baudrate= int(SPEED),
                parity= par,
                stopbits=int(STOP),
                bytesize=int(BITS),
                timeout=10
                )
        
            self.ser.isOpen()
        except exceptions.NetConfError as error:
            self.info_label["not connected"] = error.__class__.__name__
            print ("not connected")   
    def command(self,instruction):
            
        inp = instruction
        if inp == 'close':
            self.ser.close()
            exit()
        else:
            # send the character to the device
            command = inp + '\r'
            self.ser.write(command.encode())
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1).decode()

        if out != '':
            print (out)
