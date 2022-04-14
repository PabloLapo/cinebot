from typing import Union
import numpy as np
import cv2
from tracker import Tracker
from trajectory import *


class Vector:
    """Simple vector class for do operations.

    Args:
        x: value of x component
        y: value of y component
    """
    def __init__(self, x: Union[int, float] = 0.0 , y: Union[int, float] = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Built-in for add two vectors."""
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return str((self.x, self.y))

    def getPoint(self) -> tuple:
        """Returns the vector components as a tuple."""
        return self.x, self.y
    
    def setPoint(self, x: Union[int, float] = 0.0 , y: Union[int, float] = 0.0):
        """Updates the values of x and y components of the vector."""
        self.x = x
        self.y = y
    
    @staticmethod
    def distance(point0: tuple, point1: tuple) -> float:
        """Calculates the distance between two points.
        
        Args:
            point0: initial point
            point1: final point
        """
        x0, y0 = point0
        x1, y1 = point1
        distance = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        return distance

    def distanceTo(self, vector) -> float:
        """Calculates the distance between two vectors.

        Args:
            vector: A instance of Vector class
        """
        point0 = self.getPoint()
        point1 = vector.getPoint()
        return self.distance(point0, point1)

    def angleTo(self, vector) -> float:
        """Calculates the angle between two vectors.

        Args:
            vector: A instance of Vector class
        """
        try:
            x0, y0 = self.getPoint()
            x1, y1 = vector.getPoint()
            displacement = (x1 - x0, y1 - y0)
            x, y = displacement
            angle = np.arctan2(x, y)
            if x >= 0 and y >= 0:
                return angle
            if x < 0 and y >= 0:
                return angle + np.pi
            if x < 0 and y <= 0:
                return np.pi/2 - angle
            if x > 0 and y <= 0:
                return angle + np.pi
        except Exception as e:
            print(f"vector:: {e}")
            return 0


class Robot:
    """This class controls a robot with opencv.
    It uses two colors, one for positionated the robot, other as a target.
    
    Args:
        color1: [[limit_1], [limit_2]] -> [[0, 0, 0], [255, 255, 255]]
        color2: [[limit_1], [limit_2]]
        angularSpeedConstant: proportional constant for angular speed control
        linearSpeedConstant: proportional constant for linear speed control
        proximityLimit: proximity limit to be near of the targets.
    
    """
    def __init__(self, 
        color1=[[101, 73, 113], [134, 255, 255]], 
        color2=[[0, 161, 121], [184, 239, 255]],
        angularSpeedConstant = 0.7,
        linearSpeedConstant = 0.1,
        proximityLimit = 10,
        compassSensibility = 0.1,
        *args, 
        **kwargs):
        self.position = Vector(0, 0)
        self.compass = Vector(1, 1)
        self.chargePosition = getChargePoint()
        self.compassAngle = 0
        self.distanceToTarget = 0
        self.trackerBlue = Tracker(*color1)
        self.trackerRed = Tracker(*color2)
        self.trajectory = []
        self.currentIndexTrajectory = 0
        self.angularSpeed = 0
        self.linearSpeed = 0
        self.angularSpeedConstant = angularSpeedConstant
        self.linearSpeedConstant = linearSpeedConstant
        self.proximityLimit = proximityLimit
        self.compassSensibility = compassSensibility
        self.mode = "positionate"
        self.stop = True
        self.updateTrajectory()

    def speedToZero(self):
        self.angularSpeed = 0
        self.linearSpeed = 0

    def setStop(self, stop: bool = True):
        """Updates the stop status."""
        self.stop = stop
        self.speedToZero()

    def setMode(self, mode: str = "positionate"):
        """Updates the move mode of the robot.

        Args:
            mode: `positionate` or `trajectory`
        """
        self.mode = mode
        self.stop = False
        print("mode: ", mode)

    def isStop(self):
        """Checks if stop flag is true."""
        return self.stop

    def drawTrajectory(self, image: np.ndarray):
        """Draws the current trajectory over an image."""
        names = ["A", "B", "C", "D", "E"] # points names
        self.trackerBlue.draw_origin(image, text="O(0,0)", radius=2)
        for i in range(len(self.trajectory)):
            point, text = self.trajectory[i], names[i]
            text = f"{text}{point}"
            self.trackerBlue.draw_text_point(
                image, point=point, text=text, point_color=(255, 50, 100), 
                text_color=(250, 250, 250),font_scale=0.666, thickness=1, radius=5,
                translate=True,
            )

    def updateTrajectory(self):
        """Updates the current trajectory."""
        self.trajectory = getRandomTrajectory()
        self.resetTrajectoryIndex()
    
    def getCurrentTrajectoryPoint(self):
        """Returns the current target trajectory point."""
        if len(self.trajectory) > 0:
            return self.trajectory[self.currentIndexTrajectory]

    def updateCompassAngle(self, image: np.ndarray):
        """Calculates the compass angle."""
        if image is not None:
            self.position.setPoint(*self.trackerBlue.find_position(image))
            self.compass.setPoint(*self.trackerRed.find_position(image))
            self.compassAngle = self.position.angleTo(self.compass)

    def drawPositionInfo(self, image: np.ndarray):
        """Draws position info."""
        position = self.trackerBlue.get_position()
        compass = self.trackerRed.get_position()
        positionTranslated = self.trackerBlue.get_transalated_position()
        compassTranslated = self.trackerRed.get_transalated_position()
        self.trackerBlue.draw_text_point(image, positionTranslated, text="R", translate=False)
        self.trackerRed.draw_text_point(image, compassTranslated, text="G", translate=False)

    def adjustAngularSpeed(self):
        """Adjusts the rotation speed (angular speed) of the robot and sets the linear speed to 0."""
        kw, _ = self.angularSpeedConstant, self.linearSpeedConstant
        self.angularSpeed = kw * self.compassAngle
        self.linearSpeed = 0

    def adjustAngularAndLinearSpeed(self):
        """Adjusts the linear speed and the angular speed of the robot."""
        kw, kl = self.angularSpeedConstant, self.linearSpeedConstant
        self.angularSpeed = kw * self.compassAngle
        self.linearSpeed = kl

    def nextTrajectoryPoint(self):
        """Updates the current trajectory point (index)."""
        self.currentIndexTrajectory += 1
        if self.currentIndexTrajectory >= len(self.trajectory):
            self.currentIndexTrajectory = len(self.trajectory)

    def resetTrajectoryIndex(self):
        """Resest the current trajectory index point."""
        self.currentIndexTrajectory = 0

    def guide(self):
        """Checks the angular orientation."""
        if self.compassAngle > self.compassSensibility:
            self.adjustAngularSpeed()
        else:
            self.adjustAngularAndLinearSpeed()

    def move(self):
        """Move the robot according to the mode."""

        # Get the current position of the robot
        currentRobotPosition = self.position.getPoint()

        # Get the current position of the target point
        if self.mode == "positionate":
            currentTargetPosition = self.trajectory[0]
        elif self.mode == "trajectory":
            currentTargetPosition = self.getCurrentTrajectoryPoint()
        elif self.mode == "charge":
            currentTargetPosition = self.chargePosition

        # Calculate the distance between the robot and the target
        currentTargetDistance = Vector.distance(currentRobotPosition, currentTargetPosition)
            
        # Checks the compass angle
        self.guide()

        # Checks if the robot is near of the target
        if currentTargetDistance <= self.proximityLimit:
            self.speedToZero()
            self.nextTrajectoryPoint()

    def control(self):
        """Applies the control algorithm."""
        if not self.isStop():
            self.move()
        else:
            self.speedToZero()

    def update(self, image: np.ndarray, *args, **kwargs):
        """Update the state of the robot."""
        # Update the current robot position
        if image is not None:
            self.updateCompassAngle(image)
            self.drawPositionInfo(image)
            self.drawTrajectory(image)
            self.control()
    
    def getControlVariables(self):
        """Returns the control variables ready to send they to the arduino."""
        # return self.angularSpeed, self.linearSpeed
        variables = f"{self.angularSpeed: .6f}, {self.linearSpeed: .6f}"
        return variables
