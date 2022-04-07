from typing import Union
import time
from collections import deque

position_1 = (0, 0)
position_2 = (10, 10)

# python typing hints

class PID:
    """A PID control.

    Args:
        kp: proportional constant
        ki: integral constant
        kd: delta constant
    """
    def __init__(self, kp: float = 0.1,  ki: float = 0.4, kd: float = 1.0, maxlen: int = 30):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.signal = deque(maxlen=maxlen)
    
    def calculate_error(self, input: list = [], output: Union[int, float, list] = []) -> float:
        """Computes the PID correction."""
        error = output - input
        pid = self.kp * error + self.ki * error + self.kd * error
        return pid


class CinecBot:
    """This the class that controls my robot.
    
    Args:
        .
        .
        .
    """
    def __init__(self, color_1: list = [], color_2: list = []):
        self.x = 0
        self.y = 0
        self.color_1 = color_1
        self.color_2 = color_2
        self.pid_x = PID()
        self.pid_y = PID()

    def move_to(self, position: list = [], wait: float = 1.0):
        """It moves my robot to a certain position.

        Args:
            position: tuple with x, y values.
        """
        distance = self.color_2 - self.color_1
        print("moving to: ", position)
    

    def update(self):
        print("Updating robot...")
    

    def walk(self, way: list = []):
        for point in way:
            self.move_to(point, wait=1)


def camera_read():
    return "reading"


def search_colors(image):
    # search...
    return image


def calculate_points(colors):
    # hard computing...w
    return colors


def get_target_points():
    image = camera_read()
    colors = search_colors(image)
    points = calculate_points(colors)


def get_random_points():
    return [(0, 0), (10, 20), (30, 5)]


robot = CinecBot()

mode = "one_point"

while True:
    points = get_target_points()
    robot.update(points)

    if mode == "one_point":
        point = (0, 0)
        robot.move_to(point)

    if mode == "line":
        list_points = get_random_points()
        robot.walk(list_points)

    time.sleep(1)

"""
# Camel Case
    class MyRobot()
    mySpeed # var
    setValueSpeed() # function

# UnderScope
    class MyRobot
    my_speed
    set_value_speed


"""