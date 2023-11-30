import cv2
import numpy as np
from players.player import Player
# from players.mln_player import Player
import threading
import time

from qibullet import Camera

from resources.mover import Mover
from resources.detector import ColorDetector

class TestPlayer(Player):
    FIND_BALL = 0
    TRACK_BALL = 1
    SHOOT_BALL = 2

    def __init__(self, name):
        Player.__init__(self)
        self.name = name
        self.detector = ColorDetector((np.array([110,50,50]), np.array([130,255,255])))

    def debug(self, string):
        print(f'[{self.name}] {string}')

    def behave(self):
        FIND_BALL = 0
        TRACK_BALL = 1
        SHOOT_BALL = 2
        state = FIND_BALL

        # start camera thread
        # self.startCamera()

        # while True:
        #     if state == self.FIND_BALL:
        #         self.debug("FIND_BALL")
        #         img_top = self.getCameraFrame('bottom')
        #         img_top = cv2.cvtColor(img_top, cv2.COLOR_RGBA2BGR)
        #         img_seg = self.segment(img_top)
        #         bbox = self.detect(img_seg)
        #         if bbox != None:
        #             # img_bbox = cv2.rectangle(img_top, bbox[0:2], bbox[2:4], color = (0, 255, 255))
        #             # cv2.imshow('bbox', img_bbox)
        #             # cv2.waitKey(1)
        #             state = TRACK_BALL
        #         else:
        #             self.move('TurnRight')
        #     elif state == self.TRACK_BALL:
        #         self.debug("TRACK_BALL")
        #         img_top = self.getCameraFrame('bottom')
        #         img_top = cv2.cvtColor(img_top, cv2.COLOR_RGBA2BGR)
        #         img_seg = self.segment(img_top)
        #         bbox = self.detect(img_seg)
        #         if bbox != None:
        #             self.debug("I see the ball")
        #             sizex = bbox[2] - bbox[0]
        #             sizey = bbox[3] - bbox[1]
        #             x = (bbox[0] + bbox[2]) / 2
        #             if x < img_top.shape[1] * 0.4:
        #                 self.debug("TurnLeft")
        #                 self.move('TurnLeft')
        #             elif x > img_top.shape[1] * 0.6:
        #                 self.debug("TurnRight")
        #                 self.move('TurnRight')
        #             else:
        #                 self.debug("Forwards")
        #                 self.move('Forwards')
        #                 if sizey < sizex:
        #                     self.move('Forwards')
        #                     state = SHOOT_BALL
        #            # cv2.imshow('bbox', img_bbox)
        #            # cv2.waitKey(0)
        #         else:
        #             state = FIND_BALL
        #     elif state == self.SHOOT_BALL:
        #         self.debug("SHOOT_BALL")
        #         self.move("Shoot")
        #         state = FIND_BALL
        # return
        time.sleep(2)

        self.mover = Mover(self.request_queue)

        while True:
            # image = self.getCameraFrame('bottom')
            # boundary = self.detector.detect(image)
            # if boundary != None:
            #     image_boundary = cv2.rectangle(image, boundary[0:2], boundary[2:4], color = (0, 255, 255))
            #     ballPosition = self.detector.getAngle(image, Camera.K_QVGA, 0.06)
            #     cv2.putText(image_boundary, f'{round(ballPosition[0], 2)}, {round(ballPosition[1], 2)}', (boundary[0], boundary[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
            #     cv2.imshow('image', image_boundary)
            #     cv2.waitKey(1)
            #     self.debug("I see the ball")
            # else:
            #     self.debug("I dont see the ball")

            self.mover.to(0.2, 0, 0)

    def segment(self, img):
        x = np.float32(img.reshape((-1,3)))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 6 # number of clusters
        ret, label, center = cv2.kmeans(x,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        img_seg = center[label.flatten()]
        img_seg = img_seg.reshape((img.shape))
        return img_seg

    def detect(self, img_seg):
        # Change the color space from BGR to HSV
        img_hsv = cv2.cvtColor(img_seg, cv2.COLOR_BGR2HSV)
        # Define the range of HSV (Hue, Saturation, Value)
        # lower = np.array([0, 50, 50]) # 0 degree
        # upper = np.array([10, 255, 255]) # 20 degree
        lower = np.array([110,50,50])
        upper = np.array([130,255,255])
        mask = cv2.inRange(img_hsv, lower, upper)

        # print(mask.shape)
        # print(img_seg[0][0].shape)

        if np.any(mask):
            # print("I see the ball")
            y, x = np.where(mask)
            bbox = [np.min(x), np.min(y), np.max(x), np.max(y)]

            img_seg = cv2.cvtColor(img_seg, cv2.COLOR_BGR2RGB)
            img_bbox = cv2.rectangle(img_seg, bbox[0:2], bbox[2:4], color = (0, 255, 255))

            cv2.imshow('Marked', img_bbox)
            cv2.waitKey(1)

            return bbox
        else:
            # print("I dont see the ball")
            return None
        
    def startCamera(self):
        self.camera_thread = threading.Thread(target=self.cameraThread)

        # Start the thread
        self.camera_thread.start()

        print("Camera thread started")

        return
    
    def cameraThread(self):
        while True:
            self.show_live_image()

    def show_live_image(self):
        img_bot = self.getCameraFrame('bottom')
        img_top = self.getCameraFrame('top')

        # Stack vertically
        img = np.vstack((img_top, img_bot))

        # Show image
        cv2.imshow('image', img)
        # cv2.imshow('image bottom', img_bot)
        cv2.waitKey(1)

        time.sleep(0.2)

        return