import cv2
import RPi.GPIO as gp
import time
import os


SHOW_FRAME = 0
NUM_FILES = 5
NUM_FRAMES_PER_FILE = 150
WIDTH = 640
HEIGHT = 480
FPS = 30



print(f'Using OpenCV version {cv2.__version__}')

date = time.strftime("%d-%b-%Y", time.localtime())
#if gp.input(31):
os.system(f'mkdir /home/pi/TestVideos/{date}')
file_folder = f'/home/pi/TestVideos/{date}'
#else:
#    file_folder = f'/home/pi/OfficialVideo/{date}'

log = open(f'{file_folder}/log.txt', 'a')

hms = time.strftime('%H-%M-%S', time.localtime())
log.write(f'{hms}\tPi was turned on\n')

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)
capture.set(cv2.CAP_PROP_FPS,FPS)

#Test Camera
if(not capture.isOpened()):
    hms = time.strftime('%H-%M-%S', time.localtime())
    log.write(f'{hms}\tCamera is not open\n')
    print(f'Camera is not open')
else:
    hms = time.strftime('%H-%M-%S', time.localtime())
    log.write(f'{hms}\tCamera is open\n')
    print(f'Camera is open')

fcc = cv2.VideoWriter_fourcc(*'XVID')

gp.setmode(gp.BOARD)
gp.setup(37,gp.IN)
gp.setup(31,gp.IN)


hms = time.strftime('%H-%M-%S', time.localtime())
log.write(f'{hms}\tWaiting for start...\n')
print('Waiting for start...')
while(not gp.input(37)):
   time.sleep(1)

hms = time.strftime('%H-%M-%S', time.localtime())
log.write(f'{hms}\tStarting Recording...\n')
print('Starting Recording')
file_num = 0
while(gp.input(37)):
    hms = time.strftime('%H-%M-%S', time.localtime())

    file_name = f'{file_folder}/{hms}VideoFile{file_num}.avi'
    writer = cv2.VideoWriter(file_name, fcc, FPS, (WIDTH, HEIGHT))

    for frame_num in range(NUM_FRAMES_PER_FILE): 
         
        rt, frame = capture.read()
        hms = time.strftime('%H-%M-%S', time.localtime())
        if not rt:
            log.write(f'{hms}\tFailed to get a frame\n')
            print("Failed to get a frame")
            time.sleep(0.03)

        
        cv2.putText(frame, str(hms), (0, 35), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
        writer.write(frame)
        #print(f'wrote frame {frame_num}')
        
        if SHOW_FRAME:
            cv2.imshow('frame', frame)

    hms = time.strftime('%H-%M-%S', time.localtime())
    log.write(f'{hms}\trelease VideoFile{file_num}\n')     
    print(f'release VideoFile{file_num}')
    writer.release()

    file_num += 1

hms = time.strftime('%H-%M-%S', time.localtime())
log.write(f'{hms}\tFinished Capturing\n')
print('Finished Capturing')

capture.release()

cv2.destroyAllWindows()

