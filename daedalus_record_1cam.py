import cv2
import RPi.GPIO as gp
import time
import os


SHOW_FRAME = 0
NUM_FILES = 5
NUM_FRAMES_PER_FILE = 90
WIDTH = 640
HEIGHT = 480
FPS = 30



print(f'Using OpenCV version {cv2.__version__}')

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)
capture.set(cv2.CAP_PROP_FPS,FPS)

#Test Camera
if(not capture.isOpened()):
    print(f'Camera is not open')

fcc = cv2.VideoWriter_fourcc(*'XVID')

gp.setmode(gp.BOARD)
gp.setup(37,gp.IN)

print('Waiting for start...')
while(not gp.input(37)):
   time.sleep(1)

print('Starting Recording')
file_num = 0
while(gp.input(37)):

    file_name = f'/home/pi/VideoFile{file_num}.avi'
    writer = cv2.VideoWriter(file_name, fcc, FPS, (WIDTH, HEIGHT))

    for frame_num in range(NUM_FRAMES_PER_FILE): 
         
        rt, frame = capture.read()
        if not rt:
            print("Failed to get a frame")
            time.sleep(0.03)

        hms = time.strftime('%H-%M-%S', time.localtime())
        cv2.putText(frame, str(hms), (0, 35), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
        writer.write(frame)
        #print(f'wrote frame {frame_num}')
        
        if SHOW_FRAME:
            cv2.imshow('frame', frame)
         
    print(f'release VideoFile{file_num}')
    writer.release()

    file_num += 1


print('Finished Capturing')

capture.release()

cv2.destroyAllWindows()

