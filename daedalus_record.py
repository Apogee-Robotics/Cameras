import cv2
import RPi.GPIO as gp
import time

SHOW_FRAME = 0
NUM_FILES = 5
NUM_FRAMES_PER_FILE = 90
WIDTH = 640
HEIGHT = 480
FPS = 30
NUM_CAMS = 1


print(f'Using OpenCV version {cv2.__version__}')

class Cam:
    def __init__(self, cam_id=0):
        self.cam_id = cam_id
        self.capture = cv2.VideoCapture(cam_id)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)
        self.capture.set(cv2.CAP_PROP_FPS,FPS)

#Camera array
cams = []

#Add additional Cameras
for cam_num in range( NUM_CAMS):
   cams.append(Cam(cam_num))


#Test Cameras
for cam_num in range(NUM_CAMS):
   if(not cams[cam_num].capture.isOpened()):
      print(f'Camera {cam_num} is not open')

fcc = cv2.VideoWriter_fourcc(*'XVID')


writer = []

# #Set up output files
# for file_num in range(NUM_FILES):   
#    for cam_num in range(NUM_CAMS):
#       file_name = f'/home/pi/cam{cam_num}_file{file_num}.avi'
#       writer.append(cv2.VideoWriter(file_name, fcc, FPS, (WIDTH, HEIGHT)))

# print("set up files")

gp.setmode(gp.BOARD)
gp.setup(37,gp.IN)

print('Waiting for start...')
while(not gp.input(37)):
   time.sleep(1)

file_num = 0
while(gp.input(37)):

   for cam_num in range(NUM_CAMS):
      file_name = f'/home/pi/cam{cam_num}_file{file_num}.avi'
      writer.append(cv2.VideoWriter(file_name, fcc, FPS, (WIDTH, HEIGHT)))

   for frame_num in range(NUM_FRAMES_PER_FILE): 
      for cam_num in range(NUM_CAMS):   
         rt, frame = cams[cam_num].capture.read()
         if not rt:
            print("Failed to get a frame")

         hms = time.strftime('%H-%M-%S', time.localtime())
         cv2.putText(frame, str(hms), (0, 35), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
         writer[file_num*NUM_CAMS+cam_num].write(frame)
         
         if SHOW_FRAME:
            cv2.imshow('frame', frame)

         if cv2.waitKey(1) == ord('q'):
            break

   for cam_num in range(NUM_CAMS):         
      writer[file_num*NUM_CAMS+cam_num].release()

   file_num += 1


for cam_num in range(NUM_CAMS):
   cams[cam_num].capture.release()

cv2.destroyAllWindows()

