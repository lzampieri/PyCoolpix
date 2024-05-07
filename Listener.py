from .constants import *

def readByteSafeWrapper(ser):
    readed = ser.read(1)   # Read a byte
    if (len(readed) == 0):
        return TIMEOUT
    return readed[0]


def read(ser):
    readed = readByteSafeWrapper(ser)   # Read a byte

    # Autoskip FF
    while (readed == TERMINATION):
        readed = readByteSafeWrapper(ser)

    if (readed in CAMERA_EVENTS or readed in SERIAL_EVENTS):
        return readed

    if (readed in DATA_PREFIXES):
        return read_data(ser, readed)

    return UNKNOWN

def read_data(ser, readed):
    done = False
    sequence = 0
    payload = bytearray()

    while(not done):
        if( readed == LAST_DATA_PACKET ):
            done = True

        readed = int( readByteSafeWrapper(ser) )
        if( readed == sequence ):
            print(f"Reading sequence {readed}")
            sequence = sequence + 1
        else:
            print(f"Error: a sequence is missing ({readed} instead of {sequence}). Ignoring...")
            sequence = readed + 1
        
        length = int( readByteSafeWrapper(ser) + ( readByteSafeWrapper(ser) << 8 ) )

        if( length == 4 and len(payload) == 0 ): # Means is a 32 bit integer
            out = 0
            for i in range( 0, length ):
                out = out + ( readByteSafeWrapper(ser) << ( 8 * i ) )
            done = True
            payload = out
            print("Payload 32 bit integer")
        else:
            for i in range( 0, length ):
                payload.append( readByteSafeWrapper(ser) )
        
        # Read and ignore checksum
        readByteSafeWrapper(ser)
        readByteSafeWrapper(ser)
    
        # Send ACK
        ser.write(bytes( [ACK] ) )

        if( not done ):
            readed = readByteSafeWrapper(ser)
    
    return payload



def readExpected(ser, expected_sequence, max_timeout=20):

    i = 0

    while (max_timeout > 0 and i < len(expected_sequence)):

        readed = read(ser)

        if( type(readed) != int ):
            return False

        if (readed == expected_sequence[i]):
            print(f"Received {hex(readed)} :ok:")
            i += 1
        elif (readed == TIMEOUT):
            max_timeout -= 1
        else:
            print(f"Received {hex(readed)} :wrong:")
            return readed

    if (i == len(expected_sequence)):
        return ACTION_COMPLETE

    return TIMEOUT