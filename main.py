"""This is the main file."""
from cinebot.pyArduino import *

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import serial.tools.list_ports
from cinebot.libreria_ingenimundo import*
import cv2
import numpy as np
import sys

import math
from cmath import sqrt,exp
from cinebot.Origen import *
from cinebot.pydatos import *
from pydatos1 import *
from pydatos2 import *
from pydatos3 import *
import random
import math, sys, time

def stop():
    
    global isRun
    isRun = False
    global isLoad
    isLoad = False
    global isU
    isU=False

def start():
    
    global isRun
    isRun = True
   
    
    isU=False
def Ubicar():
    global isU
    isU=True
    
def trayectory():
    global hxd
    global hyd
    global hxo
    global hyo
    global hxdo
    global hydo
    global valtext
    global hydp
    global k

    k = 0
    ### ORIGEN ALETARORIO##
    xo1=83
    yo1=-76
    tyO1=ori(xo1,yo1)
    ###
    xo2=60
    yo2=-76
    tyO2=ori(xo2,yo2)
    ###
    xo3=109
    yo3=-76
    tyO3=ori(xo3,yo3)
    ###
    xo4=109
    yo4=-53
    tyO4=ori(xo4,yo4)
    ###
    xo5=109
    yo5=-99
    tyO5=ori(xo5,yo5)
    ###
    xo6=83
    yo6=-99
    tyO6=ori(xo6,yo6)
    ####
    xo7=83
    yo7=-53
    tyO7=ori(xo7,yo7)
    ###
    xo8=60
    yo8=-53
    tyO8=ori(xo8,yo8)
    ###
    xo9=60
    yo9=-99
    tyO9=ori(xo9,yo9)
    ####fin coordenadas de origen###
    
##    ###tray1ectoria 8###
    x=35
    y=-32
    x1=35
    y1=-124
    x2=110
    y2=-124
    x3=108
    y3=-32
    ty101=cuatro(x,y,x1,y1,x2,y2,x3,y3)
##    ###trayectoria 9###
    x9=35
    y9=-32
    x19=35
    y19=-101
    x29=133
    y29=-99
    x39=131
    y39=-52
    ty102=cuatro(x9,y9,x19,y19,x29,y29,x39,y39)
#####trayectoria 16###
    x052=35
    y052=-32
    x1052=35
    y1052=-76
    x2052=35
    y2052=-124
    x3052=134
    y3052=-124
    ty103=cuatro(x052,y052,x1052,y1052,x2052,y2052,x3052,y3052)
#####trayectoria 17###
    x41=134
    y41=-124
    x141=83
    y141=-124
    x241=83
    y241=-32
    x341=35
    y341=-32
    ty104=cuatro(x41,y41,x141,y141,x241,y241,x341,y341)
#####trayectoria 5###
    x51=35
    y51=-124
    x541=107
    y541=-32
    x542=108
    y542=-77
    x543=109
    y543=-124
    ty105=cuatro(x51,y51,x541,y541,x542,y542,x543,y543)
#############################
    valores=[ty101,ty102,ty103,ty104,ty105]
    data=random.choice(valores)
    ###
    text1=["A","B"]
    text2=["B","C"]
    text3=["C","D"]
    texa=[text1,text2,text3]
    valtext=random.choice(texa)
    ##
    valores_o=[tyO1,tyO2,tyO3,tyO4,tyO5,tyO6,tyO7,tyO8,tyO9]
    data_o=random.choice(valores_o)
    ret, frame = cap.read() # Leer Frame
    frame = frame[20:455, 50:520]
    alto = frame.shape[0]
    largo=frame.shape[1]
    hxdm=data[2]
    hydm=data[3]
    hxo=data_o[0]
    hyo=data_o[1]
    if len(hxdm) > 1:
        hxd = []
        hyd = []
        hxdo = []
        hydo = []
        for i in range(len(hxdm)):
            hxd.append(int(hxdm[i]*largo/distancia_x))
            hyd.append(int(hydm[i]*alto/distancia_y))
        for i in range(len(hxo)):
            hxdo.append(int(hxo[i]*largo/distancia_x))
            hydo.append(int(hyo[i]*alto/distancia_y))
def load():
    global hxd
    global hyd
    global hxdp
    global hydp
    global k
    k = 0
    x9=35
    y9=-124
    x19=35
    y19=-77
    x29=107
    y29=-77
    x39=109
    y39=-124
    yy=cuatro(x9,y9,x19,y19,x29,y29,x39,y39)

    ret, frame = cap.read() # Leer Frame
    frame = frame[20:455, 50:520]
    alto = frame.shape[0]
    largo=frame.shape[1]
    hxdm=yy[2]
    hydm=yy[3]
    if len(hxdm) > 1:
        hxdp = []
        hydp = []
        hxd = []
        hyd = []
        for i in range(len(hxdm)):
            hxd.append(int(hxdm[i]*largo/distancia_x))
            hyd.append(int(hydm[i]*alto/distancia_y))        
        

### trayextoria tres puntos ###
def ori(x,y):
    val = roboticsO()
    yy=val.valores(x,y)
    return (yy[0],yy[1])
def tres(x,y,x1,y1,x2,y2):
    v=0.1
    val = robotics1()
    yy=val.valores(x,y,x1,y1,x2,y2,v)
    return (yy[0],yy[1],yy[2],yy[3])

### trayextoria cuatro puntos ###
def cuatro(x,y,x1,y1,x2,y2,x3,y3):
    v=0.1
    val2 = robotics2()
    yy=val2.valores(x,y,x1,y1,x2,y2,x3,y3,v)
    return (yy[0],yy[1],yy[2],yy[3])

### trayextoria cinco puntos ###
def cinco(x,y,x1,y1,x2,y2,x3,y3,x4,y4):
    v=0.1
    val3 = robotics3()
    yy=val3.valores(x,y,x1,y1,x2,y2,x3,y3,x4,y4,v)
    return (yy[0],yy[1],yy[2],yy[3])
def onClossing():
    if arduino != None:
        arduino.sendData([0,0])
        arduino.close()
        
    root.quit()         #Salir del bucle de eventos.
    cap.release()       #Cerrar camara
    print("Camara desconectada")
    root.destroy()      #Destruye la ventana creada
    

    
    
def callback():
        ################## Adquisición de la Imagen ############
        ret, frame = cap.read() # Leer Frame
        frame = frame[20:455, 50:520]
       
        if ret:
            global k
            global valtext
            global pos
            global v_R
            global v_L
            Robot_dif_X, Robot_dif_Y, Robot_dif_teta ,isObject= Vision_Artificial(frame,Azul_m, Azul_M,Robot_dif)
            Robot_dif.X   =Robot_dif_X
            Robot_dif.Y   =-Robot_dif_Y
            Robot_dif.teta =Robot_dif_teta
            isObject=isObject
            traza_Robot(frame,Robot_dif)
            text=["A","B","C","D"]
        
            for i in range(len(hxd)):
                cv2.circle(frame,(hxd[i],-hyd[i]),10,RED,-1)
                cv2.putText(frame, text[i], (hxd[i], -hyd[i]),cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 200, 200), 2)
            for i in range(len(hxdo)):
                cv2.circle(frame,(hxdo[i],-hydo[i]),10,BLUE,-1)
                cv2.putText(frame, "o", (hxdo[i], -hydo[i]),cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 200, 200), 2)
            sms6.config(text = '¿Su velocidad en el tramo {} y {}?'.format(valtext[0],valtext[1]))
            sms7.config(text = '¿Su rapidez en el tramo {} y {}?'.format(valtext[0],valtext[1]))
            
            cv2.line(frame,(35,30),(426,25), (0,0,255),1)#arriba
            cv2.line(frame,(35,30),(26,430), (0,0,255),1)#derecha
            cv2.line(frame,(26,430),(440,425), (0,0,255),1)#abajo
            cv2.line(frame,(426,25),(440,425), (0,0,255),1)#izquirda
            ##intermedio
            ##    ###
            cv2.line(frame,(165,30),(165,427), (0,0,255),1)
            cv2.line(frame,(295,28),(305,427), (0,0,255),1)
            ##
            cv2.line(frame,(30,155),(430,150), (0,0,255),1)
            cv2.line(frame,(30,290),(435,287), (0,0,255),1)
            ##    ## mitad
            cv2.line(frame,(97,30),(93,427), (0,0,255),1)
            cv2.line(frame,(229,30),(231,427), (0,0,255),1)
            cv2.line(frame,(357,25),(374,427), (0,0,255),1)
            ##
            cv2.line(frame,(35,90),(426,90), (0,0,255),1)
            cv2.line(frame,(30,222),(430,220), (0,0,255),1)
            cv2.line(frame,(28,360),(438,356), (0,0,255),1)
            if isObject:            
                #Ganancias de control
                kp_w=0.7
                kp_vL=0.1
                if isRun:
                    if arduino != None:
                            arduino.sendData([uRef.get(),wRef.get()])
             
##--------------------------------------------------------------------------------------------------------------------------------------------------
                
                    if k < len(hxd):
                        R_A_1=[hxd[k]-Robot_dif.X,hyd[k]-Robot_dif.Y]
                        alfa_1=ajusta_angulo(R_A_1)
                        vec_e_w_1=error_angular(alfa_1,Robot_dif.teta)####
                        e_w_1=filtra_angulo(vec_e_w_1)###
                        sentido_1=vec_e_w_1[1]
                        e_pos_1= pow((float(hxd[k]-Robot_dif.X)*(float(hxd[k]-Robot_dif.X))) +(float(hyd[k]-Robot_dif.Y)*float(hyd[k]-Robot_dif.Y)),0.5)
                       
                        if e_w_1 >0.1:###control de orientacion
                            v_R=(kp_w*e_w_1*sentido_1*-1)
                            v_L=0
                            
                        else:
                            v_L=0.1
                            v_R=(0.6*e_w_1*sentido_1*-1)
                    
                        #condicional que pregunta si ya llegamos
                        if e_pos_1 <10:
                            uRef.set(0)
                            wRef.set(0)
                            k=k+1

                        uRef.set(v_L)
                        wRef.set(v_R)
                        
                    else:
                        uRef.set(0)
                        wRef.set(0)
                ####Control para posicionar####
                elif isU:
                    if arduino != None:
                            arduino.sendData([uRef.get(),wRef.get()])
               
##--------------------------------------------------------------------------------------------------------------------------------------------------
                
                    if k < len(hxd):
                        R_A_1=[hxd[0]-Robot_dif.X,hyd[0]-Robot_dif.Y]
                        alfa_1=ajusta_angulo(R_A_1)
                        vec_e_w_1=error_angular(alfa_1,Robot_dif.teta)####
                        e_w_1=filtra_angulo(vec_e_w_1)###
                        sentido_1=vec_e_w_1[1]
                        e_pos_1= pow((float(hxd[0]-Robot_dif.X)*(float(hxd[0]-Robot_dif.X))) +(float(hyd[0]-Robot_dif.Y)*float(hyd[0]-Robot_dif.Y)),0.5)
                       
                        if e_w_1 >0.1:###control de orientacion
                            v_R=(kp_w*e_w_1*sentido_1*-1)
                            v_L=0
                        
                        else:
                            v_L=0.1
                            v_R=(0.6*e_w_1*sentido_1*-1)
                       
                        #condicional que pregunta si ya llegamos
                        if e_pos_1 <10:
                            uRef.set(0)
                            wRef.set(0)
                            k=k+1

                        uRef.set(v_L)
                        wRef.set(v_R)
                        
                    else:
                        uRef.set(0)
                        wRef.set(0)
##-------------------------------fin----------------------------------------------------------------------------------------------------------------    
                else:
                    if arduino != None:
                        arduino.sendData([0,0])
                    k = 0

            else:
                if arduino != None:
                    arduino.sendData([0,0])
           
            # Mostrar imagen en el HMI 
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
            img = Image.fromarray(img)
            img.thumbnail((400,400))
            tkimage = ImageTk.PhotoImage(img)
            label.configure(image = tkimage)
            label.image = tkimage
        else:
            onClossing()

        
        root.after(60,callback)

####################### Control de posicion ###################
isPosition = False
isU=False
k=0
########################### Ip Cam ###########################
cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("Camara iniciada")
else:
    sys.exit("Camara desconectada")

ret, frame = cap.read()
frame = frame[20:455, 50:520]
alto = frame.shape[0]
largo=frame.shape[1]
distancia_x=170
distancia_y=150
v_R=0
v_L=0
####################### Desired position in pixels ##############
#constantes universales
isRun = False
radio=10
ti=0;
proceso='after#0'
#Definimos los Robots con sus pocisiones Iniciales
Robot_dif=Robot(RED,0,0,pi/2,radio)
k=0
# 374Xcm, -230Ycm
###trayectoria 1###
v=0.1
x=[0]
y=[0]
hxo=[0]
hyo=[0]
#Transformar el objetivo a pixeles
hxd=[]
hyd=[]
hxdo=[]
hydo=[]
hxdp=[]
hydp=[]
valtext=['A','B']
for i in range(len(x)):
    hxd.append(int(x[i]*largo/distancia_x))
    hyd.append(int(y[i]*alto/distancia_y))
for i in range(len(hxo)):
    hxdo.append(int(hxo[i]*largo/distancia_x))
    hydo.append(int(hyo[i]*alto/distancia_y))
######################### Punto de Carga ############
isLoad = False
xL = 0.5
yL = 0


############################## HMI design #################
arduino = None

root = Tk()
root.protocol("WM_DELETE_WINDOW",onClossing)
root.title("CINEBOT") # titulo de la ventana

##################### Camara ####################
label = Label(root)
label.place(x=20, y=20)

############# Puerto serial #############
port='/dev/cu.usbserial-1460'
arduino=serialArduino(port)
arduino.readSerialStart()

########### Monitoreo de velocidades ##########
uRef = DoubleVar(root,0)
varU = StringVar(root,"CINEBOT")        
labelU = Label(root, textvariable = varU)
labelU.place(x=448, y=10)
desc = Label(root, text = "Para el robot determine lo siguiente:")
desc.place(x=448, y=10)
wRef = DoubleVar(root,0)
phi = DoubleVar(root,0)
#### control para respuestas###p1 = StringVar(root, value = "¿En 5 segundos,"
sms = Label(root, text = "¿Qué posición alcanza en n1, n2 y n3 segundos?")
sms.place(x=448, y=50)

sms2 = Label(root, text = "¿Cuál fue su desplazamiento total?")
sms2.place(x=448, y=70)

sms3 = Label(root, text = "¿Cuánto se desplazó entre n1 y n2 segundos?")
sms3.place(x=448, y=90)

sms4 = Label(root, text = "¿Cuál fue su recorrido total?")
sms4.place(x=448, y=110)

sms5 = Label(root, text = "¿Cuánto recorrió entre n1 y n2 segundos?")
sms5.place(x=448, y=130)

sms6 = Label(root, text = "¿Su velocidad en el tramo A y B?")
sms6.place(x=448, y=150)

sms7 = Label(root, text = "¿Su rapidez en el tramo A y B?")
sms7.place(x=448, y=170)

############## Botones de control #############
buttonP = Button(text="Posicionar",command=Ubicar)
buttonP.place(x=20, y=410)

buttonStop = Button(text="Parar",command=stop)
buttonStop.place(x=100, y=410)

buttonStart = Button(text="Iniciar",command=start)
buttonStart.place(x=150, y=410)

buttonLoad = Button(text="Cargar",command=load)
buttonLoad.place(x=210, y=410)

buttonData = Button(text="Nuevo experimento",command=trayectory)
buttonData.place(x=270, y=410)

root.configure(width=950, height=700)

root.after(100,callback) #Es un método definido para todos los widgets tkinter.
root.mainloop()
