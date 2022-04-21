import math


pi = math.pi


def fixAngleQuadrant(angle: float, components: tuple):
    """Hola."""
    x, y = components

    if x > 0 and y >= 0:
        ...
    elif x < 0 and y >= 0:
        angle += pi
    elif x < 0 and y <= 0:
        angle += pi
    elif x > 0 and y <= 0:
        angle += 2 * pi
    elif x == 0 and y >= 0:
        angle = pi / 2
    elif x == 0 and y <= 0:
        angle = 3 * pi / 2

    return angle


def limitAngleRange(self, angle: float):
    """Limits the the angle range to a max of 2 * PI."""
    if angle >= 2 * pi:
        angle -= 2 * pi
    return angle


def angularError(angle: float, target: float):
    """Calculates the angular error between two angles."""
    error = target - angle
    sign = -1
    return error, sign
