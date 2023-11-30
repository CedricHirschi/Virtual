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
        self.detector = ColorDetector((np.array([0, 50, 50]), np.array([10, 255, 255])))
        self.bbox = None

    def debug(self, string):
        print(f'[{self.name}] {string}')

    def behave(self):
        FIND_BALL = 0
        TRACK_BALL = 1
        SHOOT_BALL = 2
        state = FIND_BALL

        # start camera thread
        self.startCamera()

        while True:
            if state == self.FIND_BALL:
                self.debug("FIND_BALL")
                if self.bbox != None:
                    state = TRACK_BALL
                else:
                    self.move('TurnRight')
            elif state == self.TRACK_BALL:
                self.debug("TRACK_BALL")
                if self.bbox != None:
                    self.debug("I see the ball")
                    sizex = self.bbox[2] - self.bbox[0]
                    sizey = self.bbox[3] - self.bbox[1]
                    x = (self.bbox[0] + self.bbox[2]) / 2
                    if x < self.img_size[0] * 0.4:
                        self.debug("TurnLeft")
                        self.move('TurnLeft')
                    elif x > self.img_size[0] * 0.6:
                        self.debug("TurnRight")
                        self.move('TurnRight')
                    else:
                        self.debug("Forwards")
                        self.move('Forwards')
                        if sizey < sizex:
                            self.move('Forwards')
                            state = SHOOT_BALL
                else:
                    state = FIND_BALL
            elif state == self.SHOOT_BALL:
                self.debug("SHOOT_BALL")
                self.move("Shoot")
                state = FIND_BALL
        
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
        self.img_size = img_bot.shape

        frame = self.detector.detect(img_bot)
        self.bbox = frame

        img_framed = cv2.rectangle(img_bot, frame[0:2], frame[2:4], color = (0, 255, 255)) if frame != None else img_bot

        cv2.imshow('Live image', img_framed)
        cv2.waitKey(1)

        time.sleep(0.1)

        return