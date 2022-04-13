from typing import Union
import numpy as np
import cv2
import time
import math, sys, time



pi=math.pi
def cos(a):
    return (math.cos(a))


def sin(a):
    return (math.sin(a))

class Tracker(object):
    """A color tracker.

    Args:
        limit_1: color limit 1
        limit_2: color limit 2
        ksize: kernel size
    """

    def __init__(
        self,
        limit_1: list = [60, 140, 79],
        limit_2: list = [90, 255, 255],
        ksize: tuple = (7, 7),
        *args,
        **kwargs,
    ):
        self.limit_1 = np.array(limit_1)
        self.limit_2 = np.array(limit_2)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize)
        self.position = (0, 0)

    def parse_array(self, array: Union[list, tuple]):
        """Converts a list or a tuple to an array"""
        return np.array(array)

    def update_range(self, limit_1: list, limit_2: list):
        """Updates the color range."""
        self.limit_1 = self.parse_array(limit_1)
        self.limit_2 = self.parse_array(limit_2)

    def filter_noise(self, mask: np.ndarray):
        """Applies some operations to filter noise over an image"""
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel)
        return mask

    def color_range(self, image: np.ndarray = None):
        """Filters color of image given a range."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.limit_1, self.limit_2)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        mask = self.filter_noise(mask)
        return mask

    @staticmethod
    def get_origin(image: np.ndarray, offset: list = [0, 0]):
        """Returns the center of an image array."""
        offset_x, offset_y = offset
        shape = image.shape
        origin = (int(shape[1] / 2 - offset_x), int(shape[0] / 2 - offset_y))
        return origin

    def get_particle_position(
        self,
        image: np.ndarray,
        mask: np.ndarray,
        origin: list,
        draw_contour: bool = True,
        color_contour: np.ndarray = None,
        translate: bool = True,
    ):
        """Returns the position of the particle."""

        # Obtain contours of my tracked object
        contour, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if draw_contour:
            cv2.drawContours(
                image, contour, -1, color_contour, 2
            )  # draw the contour of my object

        x0, y0 = origin

        # calculate position with the area of the object
        try:
            max_contour = max(
                contour, key=cv2.contourArea
            )  # choose the largest element
            moments = cv2.moments(max_contour)  # calculate moments
            x = (moments["m10"] / moments["m00"])   # x position
            y =  (moments["m01"] / moments["m00"])  # y position
        except:
            x = x0
            y = y0
        position = (x, y)
        return position

    @staticmethod
    def draw_grid(
        image: np.ndarray, grid_size: list = [10, 10], grid_color: tuple = (0, 0, 0)
    ):
        """Draw grid over and image.
        Args:
            image: a numpy array
            grid_size: number of lines on x and y
            grid_color: color of the lines
        """
        height, width, _ = image.shape
        lines_x, lines_y = grid_size
        vertical_gap = width // lines_x
        horizontal_gap = height // lines_y

        # Horizontal lines
        for i in range(horizontal_gap, height, horizontal_gap):
            cv2.line(image, (0, i), (width, i), grid_color, 1, 1)

        # Vertical lines
        for j in range(vertical_gap, width, vertical_gap):
            cv2.line(image, (j, 0), (j, height), grid_color, 1, 1)

        return image

    @staticmethod
    def parse_point(point: tuple):
        """Convert tuple values to int."""
        x, y = point
        return (int(x), int(y))

    def draw_text_point(
        self,
        image: np.ndarray = None,
        point: tuple = (20, 20),
        text: str = "A",
        text_color: tuple = (255, 255, 255),
        point_color=(255, 255, 255),
        radius=10,
        offset_x: int = 10,
        offset_y: int = 10,
        font=cv2.FONT_HERSHEY_SIMPLEX,
        font_scale: float = 0.7,
        thickness=2,
    ):
        """Draws a point accompanied of a text."""
        x, y = self.parse_point(point)
        xt, yt = self.parse_point((x + offset_x, y - offset_y))
        cv2.circle(image, (x, y), radius, point_color, -1)
        cv2.putText(
            image, text, (xt, yt), font, font_scale, text_color, thickness, cv2.LINE_AA
        )
        return image
    
    def draw_line_point(
        self,
        image: np.ndarray = None,
        WHITE = (255, 255, 255),
        YELLOW=(0, 255, 255),
        x: int = 0,
        y: int = 0,
        teta: float = 0.0,
        font = cv2.FONT_HERSHEY_SIMPLEX
    ):
        """Draws a point accompanied of a text."""
        x=x
        y=y
        teta=teta
        #cv2.circle(image,(int(x+27*cos(teta)),int(y-27*sin(teta))),1,YELLOW,-1)
        
        #cv2.line(image,(x,y),(x,y),WHITE,1)
        cv2.line(image,(x,y),(int(x+30*cos(teta)),int(y-30*sin(teta))),WHITE,1)
        #cv2.putText(image, '{},{},{}'.format(x,y,int(teta*180/pi)),(x+10,y), font, 0.4,YELLOW,1,cv2.LINE_AA)
        return image

    @staticmethod
    def translate_position(position: tuple, origin: tuple):
        """Translates a position with respect to an origin."""
        x, y = position
        x0, y0 = origin
        x_fixed, y_fixed = int(x + x0), int(abs(y - y0))
        return (x_fixed, y_fixed)

    def set_position(self, position: tuple):
        """Updates the current position value."""
        self.position = position

    def get_position(self):
        """Returns the current position value."""
        return self.position

    def track(self, image: np.ndarray, *args, **kwargs):
        """Tracks an object position."""
        # Calculate Position
        mask = self.color_range(image)
        origin = self.get_origin(image)
        position = self.get_particle_position(image, mask, origin, draw_contour=False)
        position = self.parse_point(position)
        
        # Save the current position
        self.set_position(position)
        # position_translated = self.translate_position(position, origin)

        # # Draw some info over the image
        # image = self.draw_grid(image)
        # image = self.draw_text_point(image, point=origin, text=f"O(0, 0)")
        # image = self.draw_text_point(
        #     image, point=position_translated, text=f"P{position}"
        # )
        # cv2.arrowedLine(
        #     image,
        #     origin,
        #     position_translated,
        #     (255, 255, 255),
        #     2,
        #     line_type=8,
        #     tipLength=0.3,
        # )

        return image
    
    def draw_trayec(self,image: np.ndarray = None, hxd: int=0, hyd: int=0):
        for i in range(len(hxd)):
                cv2.circle(image,(hxd[i],-hyd[i]),10,(0,0,255),-1)