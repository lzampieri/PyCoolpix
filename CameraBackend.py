from . import ListenerInterface, SenderInterface

class CameraBackend(ListenerInterface.ListenerInterface, SenderInterface.SenderInterface):

    def __init__(self):
        self.connected = False
        self.baudrate = 19200

    
    def goHighSpeed(self):
        # Speeds:
        # 1: 9600
        # 2: 19200
        # 5: 115200
        # 6: 230400

        self.sendIntroduction(self.ser, high_speed=True)

    def connect(self, port):