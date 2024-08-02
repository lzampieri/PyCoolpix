from PIL import Image
import os
from datetime import datetime
import io

class ImageRef:
    def __init__(self):
        self.img = None

    @staticmethod
    def fromBytes(data, save = True):

        img_bpm = Image.open( io.BytesIO( data ) ) # todo da sistemare

        path = os.getcwd() + datetime.now().strftime("/%Y%m%d/")
        count = 0
        while( 1 ):
            filename = f"NKIM{count:04d}.png"
            if( not os.path.exists( path + filename ) ):
                break
            count = count + 1


        os.makedirs( path, exist_ok=True )
        img_bpm.save( path + filename )