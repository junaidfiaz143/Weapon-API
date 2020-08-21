import os
import cv2
from datetime import date
import time

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # self.video = cv2.VideoCapture("")

    def __del__(self):
        self.video.release()

    def get_time(self):
        my_time = str(time.ctime(time.time()))
        my_time = my_time.replace(":","-")
        my_time = my_time.replace(" ", "_")

        return my_time

    def create_folder(self):
        today = date.today()
        print(str(today).split("-"))

        path = os.path.join("static/predictions", str(today))

        if not os.path.exists(path):
            os.makedirs(path)
            pistol_path = os.path.join(path, "pistols")
            os.makedirs(pistol_path)
            not_pistol_path = os.path.join(path, "not-pistols")
            os.makedirs(not_pistol_path)
            print("[INFO] FOLDER CREATED")
        else:
            print("[ERROR] CREATING FOLDER!")

        return path

    def get_frame(self):
        path = self.create_folder()

        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG or PNG in order to correctly display the
        # video stream.

        label = "pistols"

        height, width, channels = image.shape
        # image = cv2.flip(image, 1)
        cv2.putText(img=image, text="JD", org=(10, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=.5, color=(0, 255, 0))
        cv2.rectangle(image, (0, 0), (width, height), (0,0,255), 8)
        ret, jpeg = cv2.imencode(".png", image)
        cv2.imwrite(path+"/"+label+"/"+self.get_time()+"_"+label+".png", image)
        return jpeg.tobytes()