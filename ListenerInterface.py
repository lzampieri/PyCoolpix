from .constants import *

class ListenerInterface:

    def readByteSafeWrapper(self):
        readed = self.ser.read(1)   # Read a byte
        if (len(readed) == 0):
            return TIMEOUT
        return readed[0]

    def read(self):
        readed = self.readByteSafeWrapper()   # Read a byte

        # Autoskip FF
        while (readed == TERMINATION):
            readed = self.readByteSafeWrapper()

        if (readed in CAMERA_EVENTS or readed in SERIAL_EVENTS):
            return readed

        if (readed in DATA_PREFIXES):
            return self.read_data(readed)

        return UNKNOWN

    def read_data(self, readed):
        done = False
        sequence = 0
        payload = bytearray()

        while(not done):
            if( readed == LAST_DATA_PACKET ):
                done = True

            readed = int( self.readByteSafeWrapper() )
            if( readed == sequence ):
                sequence = sequence + 1
            else:
                print(f"Error: a sequence is missing ({readed} instead of {sequence}). Ignoring...")
                sequence = ( readed + 1 ) % 256
            
            length = int( self.readByteSafeWrapper() + ( self.readByteSafeWrapper() << 8 ) )

            if( length == 4 and len(payload) == 0 ): # Means is a 32 bit integer
                out = 0
                for i in range( 0, length ):
                    out = out + ( self.readByteSafeWrapper() << ( 8 * i ) )
                done = True
                payload = out
                print("Payload 32 bit integer")
            else:
                for i in range( 0, length ):
                    payload.append( self.readByteSafeWrapper() )
            
            # Read and ignore checksum
            self.readByteSafeWrapper()
            self.readByteSafeWrapper()
        
            # Send ACK
            self.ser.write(bytes( [ACK] ) )

            if( not done ):
                readed = self.readByteSafeWrapper()
        
        return payload



    def readExpected(self, expected_sequence, max_timeout=20):

        i = 0

        while (max_timeout > 0 and i < len(expected_sequence)):

            readed = self.read()

            if( type(readed) != int ):
                return False

            if (readed == expected_sequence[i]):
                print(f"Received {hex(readed)} :ok:")
                i += 1
            elif (readed == TIMEOUT):
                max_timeout -= 1
            else:
                print(f"Received {hex(readed)} :wrong:")
                return False

        if (i == len(expected_sequence)):
            return True

        return 
    