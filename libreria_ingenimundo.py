import numpy as np
import math, sys, time
import numpy as np
import cv2


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
def traza_Robot(imagen,Robot):
    x=Robot.X
    y=-Robot.Y
    teta=Robot.teta
    color=Robot.color
    r=Robot.r
    #cv2.circle(imagen,(int(x),int(y)),r,color,-1)
    cv2.circle(imagen,(int(x+27*cos(teta)),int(y-27*sin(teta))),1,YELLOW,-1)
    cv2.line(imagen,(x,y),(x+30,y),WHITE,1);
    cv2.line(imagen,(x,y),(int(x+30*cos(teta)),int(y-30*sin(teta))),WHITE,1);
    #texto
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(imagen, '{},{},{}'.format(Robot.X,Robot.Y,int(teta*180/pi)),(x+10,y), font, 0.4,YELLOW,1,cv2.LINE_AA)
    
def Vision_Artificial(imagen,  Verde_m, Verde_M,Robot_Verde,p=7):
    isObject = False
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    mask_Verde = cv2.inRange(hsv, Verde_m, Verde_M)
    #cv2.imshow("mask",mask_Verde)
    contornos ,_  = cv2.findContours(mask_Verde, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
      area = cv2.contourArea(c)
      if area > 20:
        appro = cv2.approxPolyDP(c,0.1*cv2.arcLength(c,True),True)
        nuevoContorno = cv2.convexHull(c)
        cv2.drawContours(imagen, [nuevoContorno], 0, RED, -1)
        #print (area)
        M = cv2.moments(c)
        if (M["m00"]==0):
            M["m00"]=1
        if (len(appro)==4):
            x_verde = int(M["m10"]/M["m00"])
            y_verde = int(M['m01']/M['m00'])
            isObject = True
            cv2.circle(imagen,(int(x_verde),int(y_verde)),1,RED,-1)
            if (x_verde -33 >= 0) & (y_verde -33 >= 0):
                hsv_Verde = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
                mask_Amarillo_Verde = cv2.inRange(hsv_Verde, Rojo_m, Rojo_M)
                contorno ,_  = cv2.findContours(mask_Amarillo_Verde, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                for i in contorno:
                    are = cv2.contourArea(i)
                    if are>20:
                        approx = cv2.approxPolyDP(i,0.1*cv2.arcLength(i,True),True)
                        M1 = cv2.moments(i)
                        if (M1["m00"]==0):
                            M1["m00"]=1
                        if (len(approx)==3):
                            teta=Robot_Verde.teta
                            cv2.drawContours(imagen,[i],0,BLUE,-1)
                            fi_Verde_x =int(M1['m10']/M1['m00']) 
                            fi_Verde_y =int(M1['m01']/M1['m00'])
                            cv2.circle(imagen,(int(fi_Verde_x),int(fi_Verde_y)),4,PURPLE,-1)
                            isObject = True
                            #Calculamos el angulo de orientación del robot
                            x_a_Verde=fi_Verde_x-x_verde
                            y_a_Verde=y_verde-fi_Verde_y    
                            if (x_a_Verde > 0) & (y_a_Verde > 0) & ((x_a_Verde)!=0): #Cuadrante 1
                                teta= math.atan((y_a_Verde)/(x_a_Verde))
                            if (x_a_Verde < 0) & (y_a_Verde > 0)& ((x_a_Verde)!=0): #Cuadrante 2
                                teta= pi + math.atan((y_a_Verde)/(x_a_Verde))
                            if (x_a_Verde < 0) & (y_a_Verde < 0)& ((x_a_Verde)!=0): #Cuadrante 3
                                teta= pi + math.atan((y_a_Verde)/(x_a_Verde))
                            if (x_a_Verde> 0) & (y_a_Verde < 0)& ((x_a_Verde)!=0): #Cuadrante 4
                                teta= 2*pi + math.atan((y_a_Verde)/(x_a_Verde))  #---------- teta
                            return (x_verde,y_verde,teta,isObject)
##            #cv2.imshow("Corte",mask_Amarillo_Verde)
##            moments_Amarillo_Verde = cv2.moments(mask_Amarillo_Verde)
##            #cv2.imshow("Amarillo",mask_Amarillo_Verde)
##            area_Amarillo_Verde = moments_Amarillo_Verde['m00']/1000
##            approx = cv2.approxPolyDP(area_Amarillo_Verde,0.1*cv2.arcLength(c,True),True)
##            if (area_Amarillo_Verde>2)and(len(approx)==3):
##                teta=Robot_Verde.teta
##                cv2.drawContours(imagen,[c],0,(0,0,255),1)
##                fi_Verde_x =int(moments_Amarillo_Verde['m10']/moments_Amarillo_Verde['m00']) 
##                fi_Verde_y =int(moments_Amarillo_Verde['m01']/moments_Amarillo_Verde['m00'])
##                isObject = True
##                cv2.circle(imagen,(int(fi_Verde_x),int(fi_Verde_y)),4,PURPLE,-1)
##                #Calculamos el angulo de orientación del robot
##                x_a_Verde=fi_Verde_x-x_verde
##                y_a_Verde=y_verde-fi_Verde_y    
##                if (x_a_Verde > 0) & (y_a_Verde > 0) & ((x_a_Verde)!=0): #Cuadrante 1
##                    teta= math.atan((y_a_Verde)/(x_a_Verde))
##                if (x_a_Verde < 0) & (y_a_Verde > 0)& ((x_a_Verde)!=0): #Cuadrante 2
##                    teta= pi + math.atan((y_a_Verde)/(x_a_Verde))
##                if (x_a_Verde < 0) & (y_a_Verde < 0)& ((x_a_Verde)!=0): #Cuadrante 3
##                    teta= pi + math.atan((y_a_Verde)/(x_a_Verde))
##                if (x_a_Verde> 0) & (y_a_Verde < 0)& ((x_a_Verde)!=0): #Cuadrante 4
##                    teta= 2*pi + math.atan((y_a_Verde)/(x_a_Verde))  #---------- teta
##                return (x_verde,y_verde,teta,isObject)
    return (Robot_Verde.X ,Robot_Verde.Y, Robot_Verde.teta , isObject)

def ajusta_angulo(V):
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
def error_angular(alfa,beta): #ang deseado   ,   ang real
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
def filtra_angulo(A):
    ang=A[0]
    if ang>=2*pi:
        ang=ang-2*pi
        return (ang)
    else:
        return ang
        
def ajusta_velocidad(m1):
    m1=m1*30
    
    if m1>=0: # Es  positiva  ?
        if abs(m1)>50:  # Es muy grande ?
            return ("000")
        else:
            a=m1*90/50
            b=90-int(a)
            if b>9 : # Decenas
                return("0"+str(int(b)))
            else : # unidades
                return ("00"+str(int(b)))
    else : # Es Negativo ?
        if abs(m1)>50:  # Es muy grande ?
            return ("180")
        else:
            a=m1*90/50
            b=90+int(abs(a))
            if b>99 : # centenas
                return(str(int(b)))
            else : # decenas
                return ("0"+str(int(b)))  
    
    
    
