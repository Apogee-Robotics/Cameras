import cv2
import RPi.GPIO as gp
import time
import os
#from switch_cam import switch_camera

class Adapter:
    SHOW_FRAME = 0
    WIDTH = 640
    HEIGHT = 480
    FPS = 30

    def __init__(self):
        self.setup_gpio()

        self.switch_camera('A')

        print(f'Using OpenCV version {cv2.__version__}')
        
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS,self.FPS)

        self.test_adapter()

        self.cameras = []

        for cam_id in 'AC':
            if (self.test_camera(cam_id)):
                self.cameras.append(Camera(cam_id))

    def setup_gpio(self):
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)

        gp.setup(7, gp.OUT)
        gp.setup(11, gp.OUT)
        gp.setup(12, gp.OUT)

    def test_adapter(self):
        if(not self.cap.isOpened()):
            print(f'Adapter is not connected')
        else:
            print(f'Adapter connection is good')

    #FIXME doesn't actually test cam, just tests adapter
    def test_camera(self, cam_id):
        self.switch_camera(cam_id)
        rt, frame = self.cap.read()
        if not rt:
            print(f'Cam {cam_id} not working')
            return False
        else:
            return True

  
    def create_writers(self, file_num):
        for cam in self.cameras:
            cam.create_writer(file_num)

    def record_frame(self):
        for cam in self.cameras:
            self.switch_camera(cam.cam_id)
            
            #self.cap.read()
            rt, cam.frame = self.cap.read()
            if not rt:
                print("Failed to get a frame")

            hms = time.strftime('%H-%M-%S', time.localtime())
            cv2.putText(cam.frame, str(hms), (0, 35), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
            cam.writer.write(cam.frame)
            #time.sleep(0.09)

            
            if self.SHOW_FRAME:
                cv2.imshow('frame', frame)

    def close_writers(self):
        for cam in self.cameras:
            cam.close_writer()

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def switch_camera(self, cam = 'A'):

        if cam == 'A':
            i2c = "i2cset -y 1 0x70 0x00 0x04"
            os.system(i2c)

            gp.output(7, False)
            gp.output(11, False)
            gp.output(12, True)

        elif cam == 'B':
            i2c = "i2cset -y 1 0x70 0x00 0x05"
            os.system(i2c)
            
            gp.output(7, True)
            gp.output(11, False)
            gp.output(12, True)

        elif cam == 'C':
            i2c = "i2cset -y 1 0x70 0x00 0x06"
            os.system(i2c)

            gp.output(7, False)
            gp.output(11, True)
            gp.output(12, False)

        elif cam == 'D':
            i2c = "i2cset -y 1 0x70 0x00 0x06"
            os.system(i2c)

            gp.output(7, True)
            gp.output(11, True)
            gp.output(12, False)

        print(f'Turned on Camera {cam}') 


class Camera:
   SHOW_FRAME = 0
   WIDTH = 640
   HEIGHT = 480
   FPS = 15
   
   def __init__(self, cam_id, output_dir="/home/pi", pin=37):
      self.cam_id = cam_id
      self.fcc = cv2.VideoWriter_fourcc(*'XVID')
      self.output_dir = output_dir
      self.frame = None
      #print(f'Using OpenCV version {cv2.__version__} on cam {cam_id}')

          
   def create_writer(self, file_num):
      file_name = f'{self.output_dir}/cam{self.cam_id}_file{file_num}.avi'
      self.writer = cv2.VideoWriter(file_name, self.fcc, self.FPS, (self.WIDTH, self.HEIGHT))

   def close_writer(self):
      self.writer.release()

   def close_camera(self):
        self.cam.release()
        cv2.destroyAllWindows()
         


         
if __name__ == "__main__":
    cam = Camera('C')
    cam.create_cam()
    cam.test_camera()
    for file_num in range(3):
        cam.create_writer(file_num)
        for frame_num in range(90):
            cam.record_frame()
        cam.closerWriter()

    cam.close()

