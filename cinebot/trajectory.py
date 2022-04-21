"""Trajectories for the robot."""
import random
from .vectors import Vector


# Those are a set of points (list of points) I defined for the robot, 
# It could increase
TRAJECTORIES = [
    [(35, -32), (35, 124), (110, 124), (108, 32)], # 1
    [(35, -32), (35, -101), (133, -99), (131, -52)], # 2
    [(35, -32), (35, -76), (35, -124), (134, -124)], # 3
    [(134, -124), (83, -124), (83, -32), (35, -32)], # 4
    #[(134, -124), (83, -124)], # 4
    [(35, -124), (107, -32), (108, -77), (109, -124)], # 5
]

# Those are a set of points for the origin of the plane xy
ORIGINS = [
    (83, -76),
    (60, -75),
    (109, -76),
    (109, -53),
    (109, -99),
    (83, -99),
    (83, -53),
    (60, -53),
    (60, -99)
]

# Point for charge the robot
CHARGE_POINT = (0, 0)


def scale(x, y, shape: list = None, alfa: int = 170, beta: int = 150):
    """Scales pixel distance to real world distance.
    Args:
        x: x input data
        y: y input data
        alfa: constant proportionality on x Axis on centimetters
        beta: constant proportionality on y Axis on centimetters
        toInt: convert to int the data?
    """
    height, width = shape
    x =  int (x * width / alfa)
    y = int (y * height / beta)
    return x, y


def splitAndScale(points: list, shape: list = None, alfa: float = 170, beta: float = 150,
    toInt: bool = True):
    """Scales a list of points.
    
    Args:
        points: list of points
        shape: an image shape
        alfa: constant proportionality on x Axis on centimetters
        beta: constant proportionality on y Axis on centimetters
        toInt: convert to int the data?

    Returns:
        datax: scaled data on x Axis
        datay: scaled data on y Axis
    """
    datax = []
    datay = []

    for x, y in points:
        x, y = scale(x, y, shape=shape, alfa=alfa, beta=beta)
        datax.append(x)
        datay.append(y)
    
    return datax, datay

def getRandomTrajectory() -> list:
    """Returns a random trajectory for the robot."""
    trajectory = TRAJECTORIES[3]
    return trajectory


def getRadomOrigin() -> tuple:
    """Returns a random origin for the xy plane."""
    return ORIGINS[random.randint(0, 8)]


def getChargePoint(shape: list = [435, 470], alfa: float = 170, beta: float = 150,
    asVector: bool = False):
    """Returns the charge point for the robot.
    Args:
        shape: an image shape
        alfa: constant proportionality on x Axis on centimetters
        beta: constant proportionality on y Axis on centimetters
        toInt: convert to int the data?
        asVector: return point as a Vector object?
    """
    point = scale(*CHARGE_POINT, shape=shape, alfa=alfa, beta=beta)
    if asVector:
        point = Vector(*point)
    return point


def getRamdonTrajectoryScaled() -> list:
    """Returns a scaled trajectory with respect an image shape."""
    points = getRandomTrajectory()
    trajectory = []
    x, y = splitAndScale(points=points, shape=[435, 470])
    for i in zip(x , y):
        trajectory.append(i)
    return trajectory 


class Trajectory:
    def __init__(self):
        self.index = 0
        self. points = getRamdonTrajectoryScaled()
    
    def __len__(self):
        return len(self.points)

    def __getitem__(self, index):
        return self.points[index]

    def reset(self):
        """Resets the index trajectory."""
        self.index = 0
    
    def update(self):
        """Updates the trajectory points."""
        self.points = getRamdonTrajectoryScaled()
        self.reset()

    def nextPoint(self):
        """Increases the index trajectory."""
        self.index += 1
        length = len(self.points)
        if self.index >= length:
            self.index = length

    def getCurrentPoint(self, asVector: bool = True):
        """Returns the current point of the trajectory.
        Args:
            asVector: return point as a Vector object?
        """
        point = self.points[self.index]
        if asVector:
            point = Vector(*point)
        return point

    def getPoint(self, index: int = 0, asVector: bool = True):
        """Returns a specific point of the list of points.
        Args:
            index: of the point
            asVector: return point as a Vector object?
        """
        point = self.__getitem__(index)
        if asVector:
            point = Vector(*point)
        return point
    