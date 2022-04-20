"""Trajectories for the robot."""
import random


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
    alto, largo = shape
    x =  int (x * largo / alfa)
    y = int (y * alto / beta)
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


def getRamdonTrajectoryScaled():
    points=getRandomTrajectory()
    trajectory=[]
    x, y= splitAndScale(points=points, shape=[435, 470])
    for i in zip(x , y):
        trajectory.append(i)
    return trajectory 


def getRandomTrajectory() -> list:
    """Returns a random trajectory for the robot."""
    trajectory = TRAJECTORIES[3]
    return trajectory


def getRadomOrigin() -> tuple:
    """Returns a random origin for the xy plane."""
    return ORIGINS[random.randint(0, 8)]


def getChargePoint(shape: list = [435, 470], alfa: float = 170, beta: float = 150):
    """Returns the charge point for the robot.
    Args:
        shape: an image shape
        alfa: constant proportionality on x Axis on centimetters
        beta: constant proportionality on y Axis on centimetters
        toInt: convert to int the data?    
    """
    return scale(*CHARGE_POINT, shape=shape, alfa=alfa, beta=beta)
# points = getRandomTrajectory()
# x, y= splitAndScale(points=points, shape=[435, 470])
# data=[]
# for i in zip(x , y):
#         data.append(i)
# data=data
# print(data)
# print(points)
