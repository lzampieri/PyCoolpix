import serial
from .constants import *
from . import Listener, Sender, Actions


class Camera:

    def __init__(self):
        pass

    def sendActionCommand(self, command, data=0, avoidIntro=False):
        if (not avoidIntro and not Sender.sendIntroduction(self.ser)):
            return False

        Sender.sendBytes(self.ser, Actions.actionCommand(command, data))
        if (Listener.readExpected(self.ser, [ACK, ACTION_COMPLETE]) == ACTION_COMPLETE):
            return True

        return False

    def goHighSpeed(self):
        Sender.sendIntroduction(self.ser, high_speed=True)

    def sendReadIntCommand(self, command, avoidIntro=False):
        if (not avoidIntro and not Sender.sendIntroduction(self.ser)):
            return False

        Sender.sendBytes(self.ser, Actions.readCommand(command))

        return Listener.read(self.ser)

    def sendSetIntCommand(self, command, data=0, avoidIntro=False):
        if (not avoidIntro and not Sender.sendIntroduction(self.ser)):
            return False

        Sender.sendBytes(self.ser, Actions.setIntCommand(command, data))

        if (Listener.readExpected(self.ser, [ACK]) == ACTION_COMPLETE):
            return True

        return False

    def sendReadVdataCommand(self, command, avoidIntro=False):
        if (not avoidIntro and not Sender.sendIntroduction(self.ser)):
            return False

        Sender.sendBytes(self.ser, Actions.readCommand(command))

        return Listener.read(self.ser)

    def sendCommand(self, command, data=0, avoidIntro=False):
        if (command[0] == ACTION):
            return self.sendActionCommand(command, data, avoidIntro)
        if (command[0] == READINT):
            return self.sendReadIntCommand(command, avoidIntro)
        if (command[0] == SETINT):
            return self.sendSetIntCommand(command, data, avoidIntro)
        if (command[0] == READVDATA):
            return self.sendReadVdataCommand(command, avoidIntro)
        print("ERROR: COMMAND TYPE NOT RECOGNIZED")

    def sendCommandFromHexString(self, hexString):
        payload = bytearray.fromhex(hexString)
        self.sendCommand([payload[0], payload[1]],
                         payload[2:] if len(payload > 2) else 0)

    # Commands

    def shot(self):
        return self.sendCommand(SHOT)

    def available_shots(self):
        return self.sendCommand(FRAMES_LAST)

    def clear_last_shot(self):
        return self.sendCommand(FRAMES_CLEAR_LAST)

    def download_last_shot(self):
        count = self.sendCommand(FRAMES_COUNT)
        self.goHighSpeed()
        self.sendCommand(FRAMES_SELECT, count, avoidIntro=True)
        output = self.sendCommand(FRAMES_GET, avoidIntro=True)
        with open("output.bmp", "wb") as binary_file:   
            # Write bytes to file
            binary_file.write(output)
        return len(output)


    def length_last_shot(self):
        count = self.sendCommand(FRAMES_COUNT)
        self.goHighSpeed()
        self.sendCommand(FRAMES_SELECT, count, avoidIntro=True)
        return self.sendCommand(FRAMES_GET_LENGTH, avoidIntro=True)

    def connect(self, port):  # Warning: a serial.SerialException can be generated and must be catched
        self.connected = False
        if (getattr(self, 'ser', False) and getattr(self.ser, 'is_open', False)):
            self.ser.close()

        self.ser = serial.Serial(
            port, 19200, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=1)

        if (not self.ser.is_open):
            return False

        for _ in range(5):
            Sender.sendByte(self.ser, INIT)

            while True:
                readed = Listener.read(self.ser)
                if (readed == TIMEOUT):
                    break
                if (readed == NACK):
                    self.connected = True
                    break

            if (self.connected):
                print("Camera successfully connected")
                break

        return self.connected
