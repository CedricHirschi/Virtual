from resources.motions import Motions
import time

# Forwards/Backwards ~ 10cm
FWD_BWD_STEP = 0.1
# TurnLeft/TurnRight ~ 16 degree or 0.28 radians
TURN_STEP = 0.28
# SideStepLeft/SideStepRight ~ 3cm
SIDE_STEP = 0.03

class Mover:
    """
    Class for moving robot

        Attributes:
            moveForward (list): list of tuples for moving forward
            moveBackward (list): list of tuples for moving backward
            turnLeft (list): list of tuples for turning left
            turnRight (list): list of tuples for turning right
            sideStepLeft (list): list of tuples for side stepping left
            sideStepRight (list): list of tuples for side stepping right
    """

    moveForward = Motions.getMotion("Forwards")
    moveBackward = Motions.getMotion("Backwards")
    turnLeft = Motions.getMotion("TurnLeft")
    turnRight = Motions.getMotion("TurnRight")
    sideStepLeft = Motions.getMotion("SideStepLeft")
    sideStepRight = Motions.getMotion("SideStepRight")

    def __init__(self, request_queue) -> None:
        self.speed = 1.0
        self.request_queue = request_queue
        print("Mover initialized")
        print(f'  Speed: {self.speed}')
        print(f'  Queue: {self.request_queue}')

    def setSpeed(self, speed):
        """
        Set speed of robot

            Parameters:
                speed (float): fractional speed of robot [0.0 - 1.0]

            Returns:
                None
        """
        if speed < 0.0 or speed > 1.0:
            raise ValueError("Speed must be between 0.0 and 1.0")
        
        self.speed = speed

    def _move(self, movement):
        for i in range(len(movement)):
            move = movement[i]

            self.request_queue.put(["move", move[1]])

            waitTime = 0
            if i < len(movement) - 1:
                nextMove = movement[i + 1]
                waitTime = nextMove[0] - move[0]

            time.sleep(waitTime / self.speed * 2)

    def to(self, x, y, angle):
        """
        Move robot with specific distance and angle

            Parameters:
                x (float): distance in x-axis [meters]
                y (float): distance in y-axis [meters]
                angle (float): angle to turn [radians]

            Note:
                Moves are done in order of angle, x, y

            Returns:
                None
        """
        xSteps = int(x / FWD_BWD_STEP)
        ySteps = int(y / SIDE_STEP)
        angleSteps = int(angle / TURN_STEP)

        for _ in range(angleSteps):
            if angle > 0:
                self._move(Mover.turnRight)
            else:
                self._move(Mover.turnLeft)

        for _ in range(xSteps):
            if x > 0:
                self._move(Mover.moveForward)
            else:
                self._move(Mover.moveBackward)

        for _ in range(ySteps):
            if y > 0:
                self._move(Mover.sideStepRight)
            else:
                self._move(Mover.sideStepLeft)