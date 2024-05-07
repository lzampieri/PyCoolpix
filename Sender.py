from .constants import *
from . import Listener

# SEND

def sendByte(ser, byte):
    sendBytes(ser,[byte])

def sendBytes(ser, bytes_array):
    print( f"Sending: { [ hex(b) for b in bytes_array ] }" )
    ser.write(bytes(bytes_array))


def sendIntroduction(ser, max_trials = 5, high_speed = False ):

    ser.baudrate = 19200

    while( max_trials > 0 ):

        if( high_speed ):
            sendBytes( ser, [0x00, 0x1B, 0x53, 0x06, 0x00, 0x00, 0x11, 0x06, 0x00, 0x00, 0x00, 0x17, 0x00] )
        else:
            sendBytes( ser, [0x00, 0x1B, 0x53, 0x06, 0x00, 0x00, 0x11, 0x02, 0x00, 0x00, 0x00, 0x13, 0x00] )

        if( Listener.readExpected( ser, [ NACK, ACK ], max_timeout=3 ) == ACTION_COMPLETE ):

            if( high_speed ):
                ser.baudrate = 230400
            
            return True
        
        max_trials -= 1

    return False