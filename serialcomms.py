from configurations import *
import time
import serial
# configure the serial connections (the parameters differs on the device you are connecting to)
def connect(PORT,SPEED,BITS,STOP,PARITY):
        
    if PARITY == "none": PARITY ="N"
    if PARITY == "odd": PARITY ="O"
    if PARITY == "even": PARITY ="E"
    ser = serial.Serial(
        port=PORT,
        baudrate= int(SPEED),
        parity= PARITY,
        stopbits=int(STOP),
        bytesize=int(BITS)
    )

    print (type(serial.PARITY_NONE))
    print (serial.PARITY_NONE)
    ser.isOpen()

    print ('You Are now Connected to %s \r\n Enter your commands below.\r\ntype "close" to leave the application.' % PORT )

    inp=1
    while 1 :
        # get keyboard input
        inp = input(">> ")
            # Python 3 users
            # input = input(">> ")
        if inp == 'close':
            ser.close()
            #exit()
        else:
            # send the character to the device
            # (note that I append a \r\n carriage return and line feed to the characters - this is requested by my device)
            command = inp + '\r'
            ser.write(command.encode())


            
            out = ''
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(5)
            while ser.inWaiting() > 0:
                out += ser.read(100).decode()

            if out != '':
                print (out)
 
