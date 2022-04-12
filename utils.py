import numpy as np
from tracker import Tracker

class RobotControl:
    def __init__(self):
        self.tracker_orange = Tracker()
        self.tracker_green = Tracker()
        self.count = 0
        self.count_limit = 20

    def draw_info(self, image):
        ...

    def update(self, image):
        self.tracker_orange.track(image.copy())
        self.tracker_green.track(image.copy())
        # self.draw_info(image)

    def calculate_distance(self):
        x1, y1 = self.tracker_orange.get_position()
        x2, y2 = self.tracker_green.get_position()
        distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return distance

    def getCount(self):
        return self.count


    def isReady(self):
        self.count += 1
        if self.count > self.count_limit:
            self.count = 0
            return True
        return False