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
        """Return the vector components as a tuple."""
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
    
    """
    def __init__(self, 
        color1=[[101, 73, 113], [134, 255, 255]], 
        color2=[[0, 161, 121], [184, 239, 255]],
        *args, 
        **kwargs):
        self.position = Vector(0, 0)
        self.target = Vector(1, 1)
        self.angelToTarget = 0
        self.trackerBlue = Tracker(*color1)
        self.trackerRed = Tracker(*color2)
        self.trajectory = []

    def drawTrajectory(self, image: np.ndarray):
        """Draws the current trajectory over an image."""
        names = ["A", "B", "C", "D", "E"] # points names
        self.trackerBlue.draw_origin(image, text="O(0,0)", radius=5)
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
        print(self.trajectory)
   
    def positionate(self):
        print("posicionando...")

    def update(self, image: np.ndarray, *args, **kwargs):
        """Update the state of the robot."""
        self.position.setPoint(*self.trackerBlue.find_position(image))
        self.target.setPoint(*self.trackerRed.find_position(image))
        self.angelToTarget = self.position.angleTo(self.target)
        self.drawTrajectory(image)

