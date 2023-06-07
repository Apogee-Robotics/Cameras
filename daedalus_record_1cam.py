import cv2
import RPi.GPIO as gp
import time
import os


SHOW_FRAME = False
TIME_TO_RECORD = 5
FPS = 21
NUM_FRAMES_PER_FILE = TIME_TO_RECORD * FPS
WIDTH = 1280
HEIGHT = 720




print(f'Using OpenCV version {cv2.__version__}')

time.sleep(30)

testNumFile = open("/home/pi/TestVideos/testNumber.txt", 'r')
testNum = int(testNumFile.read())
testNumFile.close()

#date = time.strftime("%d-%b-%Y", time.localtime())
#if gp.input(31):
os.system(f'mkdir /home/pi/TestVideos/test{testNum}')
file_folder = f'/home/pi/TestVideos/test{testNum}'
testNumFile = open("/home/pi/TestVideos/testNumber.txt", 'w')
testNumFile.write(f'{testNum + 1}')
testNumFile.close()
#else:
#    file_folder = f'/home/pi/OfficialVideo/{date}'

log = open(f'{file_folder}/log.txt', 'a')

hms = time.strftime('%H-%M-%S', time.localtime())
log.write(f'\tPi was turned on\n')


capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)
capture.set(cv2.CAP_PROP_FPS,FPS)


#Test Camera
if(not capture.isOpened()):
    #hms = time.strftime('%H-%M-%S', time.localtime())
    log.write(f'{hms}\tCamera is NOT open\n')
    print(f'{hms}Camera is NOT open')
else:
    #hms = time.strftime('%H-%M-%S', time.localtime())
    log.write(f'{hms}\tCamera is open\n')
    print(f'{hms}Camera is open')

fcc = cv2.VideoWriter_fourcc(*'XVID')

gp.setmode(gp.BOARD)
gp.setup(37,gp.IN)
gp.setup(31,gp.IN)


# #hms = time.strftime('%H-%M-%S', time.localtime())
# log.write(f'{hms}\tWaiting for start...\n')
# print(f'Waiting for start...')
# while(not gp.input(37)):
#     while(not gp.input(37)):
#         time.sleep(0.5)
#     time.sleep(0.5)

hms = time.strftime('%H-%M-%S', time.localtime())
log.write(f'{hms}\tStarting Recording...\n')
print(f'Starting Recording')

te_count = 0

file_num = 0
#while(gp.input(37)):
while(te_count < 21 or gp.input(37)):
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

        if te_count < 21:
            if gp.input(37):
                te_count += 1
            else:
                te_count = 0
        
        if SHOW_FRAME:
            cv2.imshow('frame', frame)
            print('showing frame')

    hms = time.strftime('%H-%M-%S', time.localtime())
    log.write(f'{hms}\trelease VideoFile{file_num}\n')     
    print(f'release VideoFile{file_num}')
    writer.release()

    file_num += 1

    
  

hms = time.strftime('%H-%M-%S', time.localtime())
log.write(f'{hms}\tFinished Capturing\n')
log.close()
print('Finished Capturing')

capture.release()

cv2.destroyAllWindows()

