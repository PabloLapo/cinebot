from typing import Union
import math
import numpy as np


class Vector:
    """An 2D vector class.

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

    def getTuple(self) -> tuple:
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
        point0 = self.getTuple()
        point1 = vector.getTuple()
        return self.distance(point0, point1)

    def displacementTo(self, vector):
        """Calculates the displacement between the current vector to another.
        Args:
            vector: A vector instance.
        """
        point0 = self.getTuple()
        point1 = vector.getTuple()
        displacement = self.displacement(point0, point1)
        displacement = Vector(*displacement)
        return displacement

    def magnitude(self) -> float:
        """Calculates the magnitude of the current vector."""
        x, y = self.getTuple()
        magnitude = np.sqrt(x ** 2 + y ** 2)
        return magnitude

    def angle(self):
        """Calculates the current vector angle."""
        return math.atan(self.y / self.x)

    def angleTo(self, vector):
        """Calculates the angle between the current vector and another vector."""
        displacement = self.displacementTo(vector)
        angle = displacement.angle()
        return angle

    @staticmethod
    def displacement(point0: tuple, point1: tuple):
        """Returns the displacement vector between two points (position vectors)"""
        x0, y0 = point0
        x1, y1 = point1
        return (x1 - x0, y1 - y0)
