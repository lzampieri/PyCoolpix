def toByteLSB( value, length):
    return [value >> 8*i & 0xFF for i in range(0, length)]

def actionCommand(command, data=0):
    intro = [0x1B, 0x43]  # it's a command, not the first

    length = 3
    data_byte = data % 256
    checksum = (sum(command, 0) + data_byte) % (0xFFFF)

    return intro + toByteLSB(length, 2) + command + [data_byte] + toByteLSB(checksum, 2)

def readCommand(command):
    intro = [0x1B, 0x43]  # it's a command, not the first

    length = 2
    checksum = sum(command, 0) % (0xFFFF)

    return intro + toByteLSB(length, 2) + command + toByteLSB(checksum, 2)

def setIntCommand(command, data = 0):
    intro = [0x1B, 0x43]  # it's a command, not the first

    length = 6
    data_bytes = toByteLSB( data, 4 )
    checksum = (sum(command) + sum(data_bytes)) % (0xFFFF)

    return intro + toByteLSB(length, 2) + command + data_bytes + toByteLSB(checksum, 2)
