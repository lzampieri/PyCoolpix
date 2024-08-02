from .constants import *

# SEND

class SenderInterface:

    def sendByte(self, byte):
        self.sendBytes([byte])

    def sendBytes(self, bytes_array):
        print( f"Sending: { [ hex(b) for b in bytes_array ] }" )
        self.ser.write(bytes(bytes_array))


    def sendIntroduction(self, max_trials = 5 ):

        # Check if alive
        while( max_trials > 0 ):
            self.sendByte( 0x00 )
            if( self.readExpected( [ NACK ], max_timeout=3 ) ):
                break
            max_trials -= 1

        # Set baudrate
        command = Builder.actionCommand( SET_SPEED, SPEED[ self.baudrate ] )
        while( max_trials > 0 ):
            self.sendBytes( command )
            if( self.readExpected( [ ACK ], max_timeout=3 ) == True ):
                break
            max_trials -= 1

            self.ser.baudrate = self.baudrate

            # if( high_speed ):
            #     sendBytes( ser, [0x00, 0x1B, 0x53, 0x06, 0x00, 0x00, 0x11, 0x06, 0x00, 0x00, 0x00, 0x17, 0x00] )
            # else:
            #     sendBytes( ser, [0x00, 0x1B, 0x53, 0x06, 0x00, 0x00, 0x11, 0x02, 0x00, 0x00, 0x00, 0x13, 0x00] )


            if( high_speed ):
                ser.baudrate = 230400
            
            return True
            
            max_trials -= 1

        return False