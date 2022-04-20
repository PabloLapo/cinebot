from logging import exception
from tkinter import E
from typing import Union
import numpy as np
import cv2
from tracker import Tracker
from trajectory import *
import math

pi= math.pi
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
        distance = pow((float(x1-x0)*(float(x1-x0))) +(float(y1-y0)*float(y1-y0)),0.5)
        #distance = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        return distance
    
    
    @staticmethod
    def distance2(point0: tuple, point1: tuple) -> float:
        """Calculates the distance between two points.
        
        Args:
            point0: initial point
            point1: final point
        """
        x0, y0 = point0
        x1, y1 = point1
        hxe = (x1-x0)
        hye =  (y1-y0)
        he = np.array([hxe, hye])
        return he

    def distanceTo(self, vector) -> float:
        """Calculates the distance between two vectors.

        Args:
            vector: A instance of Vector class
        """
        point0 = self.getPoint()
        point1 = vector.getPoint()
        return self.distance(point0, point1)

    @staticmethod
    def displacement(point0: tuple, point1: tuple):
        """Returns the displacement vector between two points (position vectors)"""
        x0, y0 = point0
        x1, y1 = point1
        return (x1 - x0, y1 - y0)
    
    @staticmethod
    def displacement1(point0: tuple, point1: tuple):
        """Returns the displacement vector between two points (position vectors)"""
        x0, y0 = point0
        x1, y1 = point1
        return (x1 - x0, y0 - y1)

    def angleTo(self, vector) -> float:
        """Calculates the angle between two vectors.

        Args:
            vector: A instance of Vector class
        """
        try:
            point0 = self.getPoint()
            point1 = vector.getPoint()
            displacement = self.displacement1(point0, point1)
            x_a_Verde, y_a_Verde = displacement
            teta = 0
            if (x_a_Verde > 0) & (y_a_Verde > 0) & ((x_a_Verde)!=0): #Cuadrante 1
                teta= math.atan((y_a_Verde)/(x_a_Verde))
                #print("1")
            if (x_a_Verde < 0) & (y_a_Verde > 0)& ((x_a_Verde)!=0): #Cuadrante 2
                teta= pi + math.atan((y_a_Verde)/(x_a_Verde))
                #print("2")
            if (x_a_Verde < 0) & (y_a_Verde < 0)& ((x_a_Verde)!=0): #Cuadrante 3
                teta= pi + math.atan((y_a_Verde)/(x_a_Verde))
                #print("3")
            if (x_a_Verde> 0) & (y_a_Verde < 0)& ((x_a_Verde)!=0): #Cuadrante 4
                teta= 2*pi + math.atan((y_a_Verde)/(x_a_Verde))
                #print("4")
            return teta
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
        color2=[[0, 173, 68], [217, 239, 255]],
        angularSpeedConstant = 0.7,
        linearSpeedConstant = 0.1,
        proximityLimit = 10,
        compassSensibility = 0.1,
        e_w_1 = 0,
        sentido_1 = 0,
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
        self.e_w_1 = e_w_1
        self.sentido_1 = sentido_1
        self.proximityLimit = proximityLimit
        self.compassSensibility = compassSensibility
        self.currentDistance = 0
        self.mode = "positionate"
        self.stop = True
        self.updateTrajectory()

    def speedToZero(self):
        """Sets speed values to zero."""
        self.angularSpeed = 0
        self.linearSpeed = 0

    def setStop(self, stop: bool = True):
        """Updates the stop status."""
        self.stop = stop
        self.speedToZero()
        self.currentIndexTrajectory = 0

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
        names = ["A", "B", "C", "D"] # points names
        # self.trackerBlue.draw_origin(image, text="O(0,0)", radius=2)
        #print("data",self.trajectory)
        #print(f"s{len(self.trajectory)} ff {len(names)}")
        for i in range(len(self.trajectory)):
            point, text = self.trajectory[i], names[i]
            text = f"{text}{point}"
            self.trackerBlue.draw_text_point(
                image, point=point, text=text, point_color=(255, 50, 100), 
                text_color=(250, 250, 250),font_scale=0.666, thickness=1, radius=5,
                translate=False,
            )

    def updateTrajectory(self):
        """Updates the current trajectory."""
        # points = getRandomTrajectory()
        # x, y= splitAndScale(points=points, shape=[435, 470])
        # self.trajectory = []
        # for i in zip(x , y):
        #         self.trajectory.append(i)
        # self.trajectory = self.trajectory
        self.trajectory = getRamdonTrajectoryScaled()
        print(f"val {len(self.trajectory)}")
        
    
        self.resetTrajectoryIndex()
    
    def getCurrentTrajectoryPoint(self):
        """Returns the current target trajectory point."""
        return self.trajectory[self.currentIndexTrajectory]
        # if len(self.trajectory) > 0:
            # try:
            #     # if self.currentIndexTrajectory > len(self.trajectory)-1:
            #     #     self.currentIndexTrajectory = len(self.trajectory)-1
            #     # return self.trajectory[self.currentIndexTrajectory]

            # except Exception as e:
            #     print("e", e)
            #     return self.trajectory[-1]

    def updateCompassAngle(self, image: np.ndarray):
        """Calculates the compass angle."""
        if image is not None:
            self.position.setPoint(*self.trackerBlue.find_position(image, translate=True))
            self.compass.setPoint(*self.trackerRed.find_position(image, translate=True))
            self.compassAngle = self.position.angleTo(self.compass)
            #print("Valor",self.compassAngle)
            #print((self.compassAngle*180)/math.pi)
    def drawPositionInfo(self, image: np.ndarray):
        """Draws position info."""
        position = self.trackerBlue.get_position()
        compass = self.trackerRed.get_position()
        positionTranslated = self.trackerBlue.get_transalated_position()
        compassTranslated = self.trackerRed.get_transalated_position()
        self.trackerBlue.draw_origin(image)
        self.trackerBlue.draw_grid(image)
        self.trackerBlue.draw_text_point(image, positionTranslated, text="R", translate=False, radius=5, 
            point_color=[250, 150, 150])
        self.trackerRed.draw_text_point(image, compassTranslated, text="G", translate=False, radius=5,
            point_color=[150, 150, 255])

    def adjustAngularSpeed(self):
        """Adjusts the rotation speed (angular speed) of the robot and sets the linear speed to 0."""
        kw, _ = self.angularSpeedConstant, self.linearSpeedConstant
        self.angularSpeed = (kw*self.e_w_1*self.sentido_1*-1)
        self.linearSpeed = 0

    def adjustAngularAndLinearSpeed(self):
        """Adjusts the linear speed and the angular speed of the robot."""
        kw, kl = self.angularSpeedConstant, self.linearSpeedConstant
        self.angularSpeed =  (kw*self.e_w_1*self.sentido_1*-1)
        self.linearSpeed = kl

    def nextTrajectoryPoint(self):
        """Updates the current trajectory point (index)."""
        self.currentIndexTrajectory += 1
        if self.currentIndexTrajectory > len(self.trajectory)-1:
            self.currentIndexTrajectory = len(self.trajectory)-1
            
            # self.trajectory = self.trajectory[self.currentIndexTrajectory]

            

    def resetTrajectoryIndex(self):
        """Resest the current trajectory index point."""
        self.currentIndexTrajectory = 0

    def checkAngle(self):
        """Checks the angular orientation."""
        if self.e_w_1 > self.compassSensibility:
            self.adjustAngularSpeed()
            #self.nextTrajectoryPoint()
        else:
            self.adjustAngularAndLinearSpeed()
            #self.nextTrajectoryPoint()

    def checkPosition(self):
        """Checks if the robot is near to the position."""
        if self.currentDistance < self.proximityLimit:
            self.speedToZero()
            self.nextTrajectoryPoint()
            #print(f"indice {self.currentIndexTrajectory}")
            
                    

    def ajusta_angulo(self,V):
        x=V[0]
        y=V[1]
        
        #Preguntar por el cuadrante de la dirección del vector
        #cuadrante1
        if ((x >0) & (y>=0)):
            teta= math.atan((y)/(x))
        #cuadrante2
        if ((x <0) & (y>=0)):
            teta= pi + math.atan((y)/(x))
        #cuadrante3
        if ((x <0) & (y<=0)):
            teta= pi + math.atan((y)/(x))
        #cuadrante4
        if ((x >0) & (y<=0)):
            teta= 2*pi + math.atan((y)/(x))
        if((x==0)&(y>=0)):
            teta=pi/2
        if((x==0)&(y<=0)):
            teta=pi+pi/2
            
        return teta
    def error_angular(self, alfa,beta): #ang deseado   ,   ang real
        #convertir a negativos
        alfa_inv=alfa-2*pi
        beta_inv=beta-2*pi
        #comparamos distancias
        #1  + , +
        d1= beta - alfa
        #2  + , -
        d2= beta - alfa_inv
        #3  - , +
        d3= beta_inv - alfa
        #4  -  , -
        d4= beta_inv - alfa_inv
        c=[d1,d2,d3,d4]
        a= [abs(d1),abs(d2),abs(d3),abs(d4)]
        b=sorted(a)
        for i in [0,1,2,3]:
            if abs(c[i])==b[0]:
                if c[i]>=0:
                    signo=1
                    return (abs(c[i]),signo)
                else:
                    signo=-1
                    return (abs(c[i]),signo)

    def filtra_angulo(self,A):
        ang=A[0]
        if ang>=2*pi:
            ang=ang-2*pi
            return (ang)
        else:
            return ang

    def move(self):
        """Move the robot according to the mode."""

        # Get the current position of the robot
        x, y = self.position.getPoint()
        currentRobotPosition = (x , -y)

        # Get the current position of the target point
        if self.mode == "positionate":
            currentTargetPosition = self.trajectory[0]
        elif self.mode == "trajectory":
            currentTargetPosition = self.getCurrentTrajectoryPoint()
        elif self.mode == "charge":
            currentTargetPosition = self.chargePosition
        #print(f"trayectoria{currentTargetPosition}")
        #print(f"robot{currentRobotPosition}")
        # Calculate the distance between the robot and the target
        #error = Vector.distance2(currentRobotPosition, currentTargetPosition)
        xt , yt = currentTargetPosition
        disp = (xt - x, yt + y)
        self.currentDisplacement = Vector.displacement(currentRobotPosition, currentTargetPosition)
        alfa_1=self.ajusta_angulo(self.currentDisplacement)
        vec_e_w_1=self.error_angular(alfa_1,self.compassAngle)
        self.e_w_1=self.filtra_angulo(vec_e_w_1)
        self.sentido_1=vec_e_w_1[1]
        self.currentDistance = Vector.distance(currentRobotPosition, currentTargetPosition)
        print(f"distance: {self.currentDisplacement} alfa: {alfa_1} vec: {vec_e_w_1} ew: {self.e_w_1} sen: {self.sentido_1}")
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
        variables = f"{self.linearSpeed}, {self.angularSpeed}"
        return variables
