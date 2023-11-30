import cv2
import numpy as np

class ColorDetector:

    def __init__(self, color) -> None:
        self.color_lower = color[0]
        self.color_upper = color[1]

    def detect(self, img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, self.color_lower, self.color_upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            cnt = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(cnt)
            return (x, y, x + w, y + h)
        else:
            return None
        
    def getAngle(self, img, cameraRes, radius: float):
        """
        Estimate the angle relative to the camera of the ball. Use the radius of the ball in the image to estimate the distance.
        """
        bbox = self.detect(img)
        if bbox is None:
            return None

        # Get the center of the ball in the image
        center = self.getCenter(bbox)

        # Get the center of the image
        center_x = cameraRes.width / 2
        center_y = cameraRes.height / 2

        # Get the distance of the ball from the center of the image
        distance_x = center[0] - center_x
        distance_y = center[1] - center_y

        apparent_radius = ((bbox[2] - bbox[0]) + (bbox[3] - bbox[1])) / 4

        # If ball is close (apparent radius is large), then the angle is small
        # If ball is far (apparent radius is small), then the angle is large
        angle_x = np.arctan(distance_x / apparent_radius)
        angle_y = np.arctan(distance_y / apparent_radius)

        return (angle_x, angle_y)

        
    def getCenter(self, bbox):
        """
        Return the center of the ball in the image
        """
        x = (bbox[0] + bbox[2]) / 2
        y = (bbox[1] + bbox[3]) / 2
        return (x, y)
