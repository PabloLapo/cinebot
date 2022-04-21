from typing import Union
import numpy as np
from cinebot.tracker import Tracker
from cinebot.vectors import Vector
from cinebot.trajectory import Trajectory, getChargePoint
from cinebot.utils import fixAngleQuadrant, limitAngleRange, angularError

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
    availableModes = ["positionate", "trajectory", "charge"]
    def __init__(self, 
        color1: list = [[101, 73, 113], [134, 255, 255]], 
        color2: list = [[0, 173, 68], [217, 239, 255]],
        angularSpeedConstant: float = 0.7,
        linearSpeedConstant: float = 0.1,
        proximityLimit: Union[int, float] = 10,
        compassSensibility: Union[int, float] = 0.1,
        e_w_1: Union[int, float] = 0,
        sentido_1: int = 0,
        *args, 
        **kwargs):
        self.position = Vector(0, 0)
        self.compass = Vector(0, 0)
        self.chargePosition = getChargePoint(asVector=True)
        self.compassAngle = 0
        self.distanceToTarget = 0
        self.trackerBlue = Tracker(*color1)
        self.trackerRed = Tracker(*color2)
        self.angularSpeed = 0
        self.linearSpeed = 0
        self.angularSpeedConstant = angularSpeedConstant
        self.linearSpeedConstant = linearSpeedConstant
        self.e_w_1 = e_w_1
        self.sentido_1 = sentido_1
        self.proximityLimit = proximityLimit
        self.compassSensibility = compassSensibility
        self.currentDistance = 0
        self.mode = "positionate"
        self.stop = True
        self.trajectory = Trajectory()

    def speedToZero(self):
        """Sets speed values to zero."""
        self.angularSpeed = 0
        self.linearSpeed = 0

    def setStop(self, stop: bool = True):
        """Updates the stop status."""
        self.stop = stop
        self.speedToZero()
        self.trajectory.reset()

    def setMode(self, mode: str = "positionate"):
        """Updates the move mode of the robot.

        Args:
            mode: `positionate` or `trajectory` or `charge`
        """
        if mode not in self.availableModes:
            raise ValueError("Not valid mode, please try with one of those: {}".format(self.availableModes))
        self.mode = mode
        self.stop = False

    def isStop(self):
        """Checks if stop flag is true."""
        return self.stop

    def drawTrajectory(self, image: np.ndarray):
        """Draws the current trajectory over an image."""
        names = ["A", "B", "C", "D"] # points names
        for i in range(len(self.trajectory)):
            point, text = self.trajectory[i], names[i]
            text = f"{text}{point}"
            self.trackerBlue.draw_text_point(
                image, point=point, text=text, point_color=(255, 50, 100), 
                text_color=(250, 250, 250), font_scale=0.666, thickness=1, 
                radius=5, translate=False
            )

    def updateTrajectory(self):
        """Updates the current trajectory."""
        self.trajectory.update()
    
    def updateCompassAngle(self, image: np.ndarray):
        """Calculates the compass angle."""
        if image is not None:
            self.position.setPoint(*self.trackerBlue.find_position(image, translate=True))
            self.compass.setPoint(*self.trackerRed.find_position(image, translate=True))
            self.compassAngle = self.position.angleTo(self.compass)

    def drawPositionInfo(self, image: np.ndarray):
        """Draws position info."""
        position = self.trackerBlue.get_position()
        compass = self.trackerRed.get_position()
        positionTranslated = self.trackerBlue.get_transalated_position()
        compassTranslated = self.trackerRed.get_transalated_position()
        self.trackerBlue.draw_origin(image)
        self.trackerBlue.draw_grid(image)
        self.trackerBlue.draw_text_point(
            image, point=positionTranslated, text="R", translate=False, radius=5, 
            point_color=[250, 150, 150]
        )
        self.trackerRed.draw_text_point(
            image, point=compassTranslated, text="G", translate=False, radius=5,
            point_color=[150, 150, 255]
        )

    def adjustAngularSpeed(self):
        """Adjusts the rotation speed (angular speed) of the robot and sets the linear speed to 0."""
        kw, _ = self.angularSpeedConstant, self.linearSpeedConstant
        self.angularSpeed = (kw * self.e_w_1 * self.sentido_1 * -1)
        self.linearSpeed = 0

    def adjustAngularAndLinearSpeed(self):
        """Adjusts the linear speed and the angular speed of the robot."""
        kw, kl = self.angularSpeedConstant, self.linearSpeedConstant
        self.angularSpeed =  (kw * self.e_w_1 * self.sentido_1 * -1)
        self.linearSpeed = kl

    def nextTrajectoryPoint(self):
        """Updates the current trajectory point (index)."""
        self.trajectory.nextPoint()

    def resetTrajectoryIndex(self):
        """Resest the current trajectory index point."""
        self.trajectory.reset()

    def checkAngle(self):
        """Checks the angular orientation."""
        if self.e_w_1 > self.compassSensibility:
            self.adjustAngularSpeed()
        else:
            self.adjustAngularAndLinearSpeed()

    def checkPosition(self):
        """Checks if the robot is near to the position."""
        if self.currentDistance < self.proximityLimit:
            self.speedToZero()
            self.nextTrajectoryPoint()

    def move(self):
        """Move the robot according to the mode."""

        # Get the current position of the robot
        x, y = self.position.getTuple()
        currentRobotPosition = (x , -y)
        currentRobotPosition = Vector(*currentRobotPosition)

        # Get the current position of the target point
        if self.mode == "positionate":
            currentTargetPosition = self.trajectory.getPoint(index=0, asVector=True)
        elif self.mode == "trajectory":
            currentTargetPosition = self.trajectory.getCurrentPoint(asVector=True)
        elif self.mode == "charge":
            currentTargetPosition = self.chargePosition # asVector: true

        displacement = currentRobotPosition.displacementTo(currentTargetPosition)
        distance = displacement.magnitude()
        

        angleTarget = self.compassAngle
        angle = displacement.angle()
        angle = fixAngleQuadrant(angle, displacement.getTuple())
        error, sign = angularError(angle, angleTarget)
        angle2 = limitAngleRange(angle)

        # Checks the compass angle
        self.checkAngle()

        # # Checks the position
        self.checkPosition()
    
    def control(self):
        """Applies the control algorithm."""
        if not self.isStop():
            self.move()
        else:
            self.speedToZero()

    def update(self, image: np.ndarray, *args, **kwargs):
        """Updates the state of the robot."""
        if image is not None:
            self.updateCompassAngle(image)
            self.drawPositionInfo(image)
            self.drawTrajectory(image)
            self.control()
    
    def getControlVariables(self):
        """Returns the control variables ready to send they to the arduino."""
        variables = f"{self.linearSpeed}, {self.angularSpeed}"
        return variables
