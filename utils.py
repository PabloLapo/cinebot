import numpy as np
from tracker import Tracker
import numpy as np
import math, sys, time
import numpy as np
import cv2
from processing import*

pi=math.pi
#BGR
BLACK =(0,0,0);WHITE=(255,255,255);GREEN=(0,255,0)
RED=(0,0,255);BLUE=(255,0,0);YELLOW=(0,255,255)
PURPLE= (120,10,80)

#Rangos de colores en HSV ----------NOCHE
                        #Hmin  Smin  Vmin
Azul_M = np.array([134, 255, 255   ], dtype=np.uint8)
Azul_m = np.array([101, 73, 113   ], dtype=np.uint8)
Rojo_M = np.array([184, 239, 255], dtype=np.uint8)
Rojo_m = np.array([0, 161, 121], dtype=np.uint8)
Verde_M = np.array([ 83   , 255  , 255   ], dtype=np.uint8)
Verde_m = np.array([39   , 52  , 88     ], dtype=np.uint8)
Amarillo_M = np.array([ 21, 250, 255   ], dtype=np.uint8)
Amarillo_m = np.array([ 0, 83, 128   ], dtype=np.uint8)

Blanco_M = np.array([ 219  , 57  , 255   ], dtype=np.uint8)
Blanco_m = np.array([ 0  , 0  , 188   ], dtype=np.uint8)
Negro_M = np.array([ 190  , 218  , 90   ], dtype=np.uint8)
Negro_m = np.array([ 0  , 0  , 0   ], dtype=np.uint8)

def cos(a):
    return (math.cos(a))


def sin(a):
    return (math.sin(a))


def traza_ejes(imagen): #diagonal
    cv2.line(imagen,(280,0),(280,390),WHITE,1);
    cv2.line(imagen,(0,195),(560,195),WHITE,1);

class Robot():
    def __init__(self, color,X,Y,teta,r) :
        self.color=color
        self.X   = X
        self.Y   = Y
        self.teta= teta
        self.r   = r


class RobotControl:
    def __init__(self):
        self.tracker_orange = Tracker( [90,185,92],[120, 255, 255])
        self.tracker_green = Tracker([60, 140, 79],[90, 239, 255])
        self.orange_x=0
        self.x_green=0
        self.y_green=0
        self.orange_y=0
        self.running=False
        self.pos=False
        self.Robot_dif=Robot(RED,0,0,pi/2,10)
        self.kp_w=0.7
        self.kp_vL=0.1
        self.v_R=0
        self.v_L=0
        self.k=0
        self.uRef = 0
        self.wRef = 0
    def isRunnig(self):
        return self.running
    
    def setRunning(self, value):
        self.running=value
    
    def isPosition(self):
        return self.pos
    
    def setPosition(self, value):
        self.pos=value

    def update(self, image):
        self.tracker_orange.track(image.copy())
        self.tracker_green.track(image.copy())
        origin=self.tracker_orange.get_origin(image)
        position1 = self.tracker_green.get_position()
        position2 = self.tracker_orange.get_position()
        self.orange_x=position1[0]
        self.x_green=position2[0]
        self.y_green=position2[1]
        self.orange_y=position1[1]
        #position1 = self.tracker_green.translate_position(position1, origin)
        #position2 = self.tracker_orange.translate_position(position2, origin)
        self.tracker_green.draw_text_point(image, point=position1, text="A")
        self.tracker_orange.draw_text_point(image, point=position2, text="B")
        
        return image
    def run(self,image):
        if image is not None:
            self.alto = image.shape[0]
            self.largo=image.shape[1]
            Robot_dif_X, Robot_dif_Y, Robot_dif_teta = self.Vision_Artificial(self.Robot_dif)
            self.Robot_dif.X   =Robot_dif_X
            self.Robot_dif.Y   =-Robot_dif_Y
            self.Robot_dif.teta =Robot_dif_teta
            #print(Robot_dif_teta)
            hxd, hyd, k =trayectory(self.largo,self.alto,170,
                    150,
                    self.puntosTrayectoria()[0],self.puntosTrayectoria()[1],self.puntosTrayectoria()[2],
                    self.puntosTrayectoria()[3],self.puntosTrayectoria()[4],self.puntosTrayectoria()[5],
                    self.puntosTrayectoria()[6],self.puntosTrayectoria()[7],self.puntosTrayectoria()[8],
                    self.puntosTrayectoria()[9],self.puntosTrayectoria()[10],self.puntosTrayectoria()[11],
                    self.puntosTrayectoria()[12],self.puntosTrayectoria()[13],self.puntosTrayectoria()[14],
                    self.puntosTrayectoria()[15],self.puntosTrayectoria()[16],self.puntosTrayectoria()[17],
                    self.puntosTrayectoria()[18],self.puntosTrayectoria()[19],self.puntosTrayectoria()[20],
                    self.puntosTrayectoria()[21],self.puntosTrayectoria()[22],self.puntosTrayectoria()[23],
                    self.puntosTrayectoria()[24],self.puntosTrayectoria()[25],self.puntosTrayectoria()[26],
                    self.puntosTrayectoria()[27],self.puntosTrayectoria()[28],self.puntosTrayectoria()[29],
                    self.puntosTrayectoria()[30],self.puntosTrayectoria()[31],self.puntosTrayectoria()[32],
                    self.puntosTrayectoria()[33],self.puntosTrayectoria()[34],self.puntosTrayectoria()[35],
                    self.puntosTrayectoria()[36],self.puntosTrayectoria()[37],self.puntosTrayectoria()[38],
                    self.puntosTrayectoria()[39])
            self.dibujar(image, hxd, hyd)
            self.traza_Robot(image, Robot_dif_X, Robot_dif_Y, Robot_dif_teta)
        if self.isRunnig():
            # if self.arduino != None:
            #         self.arduino.sendData([uRef.get(),wRef.get()])
            if self.k < len(hxd):
                R_A_1=[hxd[self.k]-self.Robot_dif.X, hyd[k]-self.Robot_dif.Y]
                alfa_1=self.ajusta_angulo(R_A_1)
                vec_e_w_1=self.error_angular(alfa_1,self.Robot_dif.teta)####
                e_w_1=self.filtra_angulo(vec_e_w_1)###
                sentido_1=vec_e_w_1[1]
                e_pos_1= pow((float(hxd[self.k]-self.Robot_dif.X)*(float(hxd[self.k]-self.Robot_dif.X))) +(float(hyd[self.k]-self.Robot_dif.Y)*float(hyd[self.k]-self.Robot_dif.Y)),0.5)
                if e_w_1 >0.1:###control de orientacion
                    self.v_R=(self.kp_w*e_w_1*sentido_1*-1)
                    self.v_L=0
                    
                else:
                    self.v_L=0.1
                    self.v_R=(self.kp_w*sentido_1*-1)
            
                #condicional que pregunta si ya llegamos
                if e_pos_1 <10:
                    self.uRef=0#setear en 0
                    self.wRef=0#setear en 0
                    self.k=self.k+1

                self.uRef=self.v_L# setear el valor a enviar
                self.wRef=self.v_R# setear el valor a enviar
                
            else:
                self.uRef=0#setear en 0
                self.wRef=0#setear en 0
            #print("inciando")
        elif self.isPosition():
            if self.k < len(hxd):
                R_A_1=[hxd[self.k]-self.Robot_dif.X, hyd[k]-self.Robot_dif.Y]
                alfa_1=self.ajusta_angulo(R_A_1)
                vec_e_w_1=self.error_angular(alfa_1,self.Robot_dif.teta)####
                e_w_1=self.filtra_angulo(vec_e_w_1)###
                sentido_1=vec_e_w_1[1]
                e_pos_1= pow((float(hxd[self.k]-self.Robot_dif.X)*(float(hxd[self.k]-self.Robot_dif.X))) +(float(hyd[self.k]-self.Robot_dif.Y)*float(hyd[self.k]-self.Robot_dif.Y)),0.5)
                if e_w_1 >0.1:###control de orientacion
                    self.v_R=(self.kp_w*e_w_1*sentido_1*-1)
                    self.v_L=0
                    
                else:
                    self.v_L=0.1
                    self.v_R=(self.kp_w*sentido_1*-1)
            
                #condicional que pregunta si ya llegamos
                if e_pos_1 <10:
                    self.uRef=0#setear en 0
                    self.wRef=0#setear en 0
                    self.k=self.k+1

                self.uRef=self.v_L# setear el valor a enviar
                self.wRef=self.v_R# setear el valor a enviar
                
            else:
                self.uRef=0#setear en 0
                self.wRef=0#setear en 0
        else:
            self.uRef=0
            self.wRef=0
            
    def getVariables(self):
        return self.uRef, self.wRef

    def Vision_Artificial(self,Robot_Verde):
        teta=Robot_Verde.teta
        x_a_Verde=self.orange_x-self.x_green
        y_a_Verde=self.y_green-self.orange_y 
        if (x_a_Verde > 0) & (y_a_Verde > 0) & ((x_a_Verde)!=0): #Cuadrante 1
            teta= math.atan((y_a_Verde)/(x_a_Verde))
        if (x_a_Verde < 0) & (y_a_Verde > 0)& ((x_a_Verde)!=0): #Cuadrante 2
            teta= pi + math.atan((y_a_Verde)/(x_a_Verde))
        if (x_a_Verde < 0) & (y_a_Verde < 0)& ((x_a_Verde)!=0): #Cuadrante 3
            teta= pi + math.atan((y_a_Verde)/(x_a_Verde))
        if (x_a_Verde> 0) & (y_a_Verde < 0)& ((x_a_Verde)!=0): #Cuadrante 4
            teta= 2*pi + math.atan((y_a_Verde)/(x_a_Verde))  #---------- teta

        return (self.x_green, self.y_green, teta)
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
    def error_angular(self,alfa,beta): #ang deseado   ,   ang real
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
    
    def traza_Robot(self, imagen, x, y, teta):
        
        #cv2.circle(imagen,(int(x),int(y)),r,color,-1)
        cv2.circle(imagen,(int(x+27*cos(teta)),int(y-27*sin(teta))),1,YELLOW,-1)
        cv2.line(imagen,(x,y),(x+100,y),WHITE,2)
        cv2.line(imagen,(x,y),(int(x+30*cos(teta)),int(y-30*sin(teta))),WHITE,2)
       
        #texto
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(imagen, '{},{},{}'.format(x,y,int(teta*180/pi)),(x+10,y), font, 1,YELLOW,1,cv2.LINE_AA)
        
        
        
    def dibujar(self,image, hxd, hyd):
        self.tracker_green.draw_trayec(image, hxd, hyd)
    
    def puntosTrayectoria(self):
        ### Trayectoria 1 ###
        xTy1p1=35
        yTy1p1=-32
        xTy1p2=35
        yTy1p2=-124
        xTy1p3=110
        yTy1p3=-124
        xTy1p4=108
        yTy1p4=-32
        ### Trayectoria 2 ###
        xTy2p1=35
        yTy2p1=-32
        xTy2p2=35
        yTy2p2=-76
        xTy2p3=35
        yTy2p3=-124
        xTy2p4=134
        yTy2p4=-124
        ### Trayectoria 3 ###
        xTy3p1=134
        yTy3p1=-124
        xTy3p2=83
        yTy3p2=-124
        xTy3p3=83
        yTy3p3=-32
        xTy3p4=35
        yTy3p4=-32
        ### Trayectoria 4 ###
        xTy4p1=35
        yTy4p1=-124
        xTy4p2=107
        yTy4p2=-32
        xTy4p3=108
        yTy4p3=-77
        xTy4p4=109
        yTy4p4=-124
        ### Trayectoria 5 ###
        xTy5p1=35
        yTy5p1=-32
        xTy5p2=35
        yTy5p2=-101
        xTy5p3=133
        yTy5p3=-99
        xTy5p4=131
        yTy5p4=-52
        return(xTy1p1,yTy1p1,xTy1p2,yTy1p2,xTy1p3,yTy1p3,xTy1p4,yTy1p4,
               xTy2p1,yTy2p1,xTy2p2,yTy2p2,xTy2p3,yTy2p3,xTy2p4,yTy2p4,
               xTy3p1,yTy3p1,xTy3p2,yTy3p2,xTy3p3,yTy3p3,xTy3p4,yTy3p4,
               xTy4p1,yTy4p1,xTy4p2,yTy4p2,xTy4p3,yTy4p3,xTy4p4,yTy4p4,
               xTy5p1,yTy5p1,xTy5p2,yTy5p2,xTy5p3,yTy5p3,xTy5p4,yTy5p4)
