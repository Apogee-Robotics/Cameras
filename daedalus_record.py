import cv2
import RPi.GPIO as gp
import time
from pi_cameras import Camera
from pi_cameras import Adapter


SHOW_FRAME = 0
#NUM_FILES = 5
NUM_FRAMES_PER_FILE = 90
#WIDTH = 640
#HEIGHT = 480
#FPS = 30
#NUM_CAMS = 1

def main():
   
   cams = Adapter()

   gp.setmode(gp.BOARD)
   gp.setup(37,gp.IN)

   try:
      print('Waiting for start...')
      while(not gp.input(37)):
         time.sleep(1)

      print('Starting Recording')
      file_num = 0
      while(gp.input(37)):
         cams.create_writers(file_num)

         for frame_num in range(NUM_FRAMES_PER_FILE):
         
            cams.record_frame()

         cams.close_writers()
         print(f'Closed file {file_num}')

         file_num += 1


      cams.close()

   except KeyboardInterrupt:
      cams.close()

if __name__ == "__main__":
   main()