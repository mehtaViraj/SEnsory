import numpy as np
import imutils
from imutils.video import VideoStream
import cv2
from collections import OrderedDict
import movement.colour.colour_ranger as labeler
import random


class CameraHandler:
    def __init__(self, ip):
        # Capturing video through webcam
        self.vs = VideoStream(src='http://{}:8080/video'.format(ip)).start()
        colors = OrderedDict({
            "dark blue": (0, 0, 255),
            #"red": (255, 0, 0),
            "green": (0, 255, 0),
            "yellow": (255, 255, 0),
            "purple": (255, 0, 255),
            #"cyan": (0, 255, 255),
            #"orange": (255, 72, 0),
            "pink": (255, 192, 203)

        })
        self.cl_hsv = labeler.ColorLabelerHSV(colors)

    def release(self):
        self.vs.release()
        cv2.destroyAllWindows()

    def find_obj(self, to_find):
        print("Looking for {}".format(to_find))
        # Reading the video from the
        # webcam in image frames
        big_frame = self.vs.read()

        new_width = 400
        frame = imutils.resize(big_frame, width=new_width)
        height = frame.shape[0]
        width = frame.shape[1]
        centre = (int(width/2), int(height/2))

        # Convert the frame in
        # BGR(RGB color space) to
        # HSV(hue-saturation-value)
        # color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsvFrame = cv2.GaussianBlur(hsv, (11, 11), 0)

        mask = self.cl_hsv.colourMasker(hsvFrame, to_find, 150, 135)

        thresh = cv2.Canny(mask, 20, 200, 255)
        # find cnts in the thresholded frame
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        cnts_centre_list = []

        for pic, contour in enumerate(cnts):
            area = cv2.contourArea(contour)
            if area < 100:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(
                frame, (x, y), (x + w, y + h),  (0, 0, 255), 2)

            cnt_centre = ((x + w/2), (y+h/2))
            cnts_centre_list.append(cnt_centre)
            #cv2.putText(frame, to_find+" - "+str(area)[:4], (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255))

        #cv2.imshow("Color Detection in Real-TIme", frame)
        return cnts_centre_list
        # # Program Termination
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #     self.vs.release()
        #     cv2.destroyAllWindows()

    def save_picture(self):
        big_frame = self.vs.read()
        path = '/home/pi/sensory/SEnsory/flaskserver/movement/saved_images/{}.jpg'.format(
            random.randint(1, 10000))

        cv2.imwrite(path, big_frame)
        print('----TOOK A PICTURE  {}----'.format(path))


# MAIN
if __name__ == '__main__':
    cam = CameraHandler("192.168.62.124")

    try:
        while True:
            objects_found = cam.find_obj("yellow")
            if len(objects_found) == 0:
                print("Not Found")
            else:
                print(objects_found)
    except KeyboardInterrupt:
        cam.release()
