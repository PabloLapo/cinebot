############## Importar modulos #####################
from pyArduino import *

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import serial.tools.list_ports
from libreria_ingenimundo import*
import cv2
import numpy as np
import sys

import math
from cmath import sqrt,exp
from pydatos import *
from pydatos1 import *
from pydatos2 import *
from pydatos3 import *
import random
import math, sys, time
def serial_ports():    
    return serial.tools.list_ports.comports()

def on_select(event=None):
    ########################### Serial communication ###########
    find_com = serial.tools.list_ports
    COM = find_com.comports()
    port = COM[portList.current()][0]
    global arduino
    arduino = serialArduino(port,sizeData=2)
    #arduino = serialArduino(port)
    arduino.readSerialStart()
    varState.set("Estado: Conectado")
    
def stop():
    global isRun
    isRun = False
    global isLoad
    isLoad = False
    
def start():
    global isRun
    global isPosition
    isRun = True
    isPosition = True
    
def trayectory():
    global hxd
    global hyd
    global hxdp
    global hydp
    global k

    k = 0

##    ###tray1ectoria 8###
    x=50
    y=-20
    x1=50
    y1=-90
    x2=50
    y2=-125
    ty101=tres(x,y,x1,y1,x2,y2)
##    ###trayectoria 9###
    x9=30
    y9=-70
    x19=120
    y19=-30
    x29=120
    y29=-120
    x39=30
    y39=-120
    ty102=cuatro(x9,y9,x19,y19,x29,y29,x39,y39)
#####trayectoria 16###
    x052=30
    y052=-120
    x1052=60
    y1052=-120
    x2052=133
    y2052=-120
    ty103=tres(x052,y052,x1052,y1052,x2052,y2052)
#####trayectoria 17###
    x41=30
    y41=-20
    x141=30
    y141=-120
    x241=133
    y241=-120
    x341=133
    y341=-30
    ty104=cuatro(x41,y41,x141,y141,x241,y241,x341,y341)
#############################
    valores=[ty101,ty102,ty103,ty104]
    data=random.choice(valores)
    ret, frame = cap.read() # Leer Frame
    frame = frame[20:455, 50:520]
    alto = frame.shape[0]
    largo=frame.shape[1]
    hxdm=data[2]
    hydm=data[3]
    if len(hxdm) > 1:
        hxd = []
        hyd = []
        for i in range(len(hxdm)):
            hxd.append(int(hxdm[i]*largo/distancia_x))
            hyd.append(int(hydm[i]*alto/distancia_y))        

def load():
    global hxd
    global hyd
    global hxdp
    global hydp
    global k
    k = 0
    xi=60
    yi=-100
    xf=157
    yf=-99
    val = robotics()
    yy=val.valores(xi,yi,xf,yf,v)
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
            global isPosition
            global pos
            global v_R
            global v_L
            Robot_dif_X, Robot_dif_Y, Robot_dif_teta ,isObject= Vision_Artificial(frame,Azul_m, Azul_M,Robot_dif)
            Robot_dif.X   =Robot_dif_X
            Robot_dif.Y   =-Robot_dif_Y
            Robot_dif.teta =Robot_dif_teta
            isObject=isObject
            traza_Robot(frame,Robot_dif)
            for i in range(len(hxd)):
                cv2.circle(frame,(hxd[i],-hyd[i]),5,RED,-1)
            
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
                kp_w=0.8
                kp_vL=0.1
                #print(e_w_1)
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
                    #    print("fal")
                    else:
                        v_L=0.1
                        v_R=0
                       # print("llegue")
                
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
                    
                    
##                

##-------------------------------fin----------------------------------------------------------------------------------------------------------------

                if isRun:
                    if arduino != None:
                        arduino.sendData([uRef.get(),wRef.get()])
                       
                else:
                    if arduino != None:
                        arduino.sendData([0,0])
                    k = 0           

##                if arduino != None:
##                    bateria = arduino.rawData[1]
            else:
                if arduino != None:
                    arduino.sendData([0,0])

            
            varU.set("Velocidad lineal: "+str(uRef.get()))
            varW.set("Velocidad angular : "+str(wRef.get()))
            varPhi.set("Orientacion: "+str((Robot_dif.teta*180)/math.pi))
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
#Definimos los Robots con sus pocisiones Iniciales
Robot_dif=Robot(RED,0,0,pi/2,radio)
k=0
# 374Xcm, -230Ycm
###trayectoria 1###
v=0.1
x=[25,149,133]
y=[-128,-128,-80]
#Transformar el objetivo a pixeles
hxd=[]
hyd=[]
hxdp=[]
hydp=[]
for i in range(len(x)):
    hxd.append(int(x[i]*largo/distancia_x))
    hyd.append(int(y[i]*alto/distancia_y))

######################### Punto de Carga ############
isLoad = False
xL = 0.5
yL = 0


############################## HMI design #################
arduino = None

root = Tk()
root.protocol("WM_DELETE_WINDOW",onClossing)
root.title("Vision Artificial") # titulo de la ventana

##################### Camara ####################
label = Label(root)
label.place(x=20, y=20)

############# Puerto serial #############
labelS = Label(root, text="Elija un puerto COM")
labelS.place(x=448, y=160)
portList = ttk.Combobox(root, values=serial_ports())
portList.place(x=450, y=180)
portList.bind('<<ComboboxSelected>>', on_select)

############## Estado de Conexion #############
varState = StringVar(root,"Estado : Desconectado")        
labelSbat = Label(root, textvariable = varState)
labelSbat.place(x=448, y=210)
########### Monitoreo de velocidades ##########
uRef = DoubleVar(root,0)
varU = StringVar(root,"Linear velocity : 0.00")        
labelU = Label(root, textvariable = varU)
labelU.place(x=20, y=400)

wRef = DoubleVar(root,0)
varW = StringVar(root,"Angular velocity : 0.00")
labelW = Label(root, textvariable = varW)
labelW.place(x=160, y=400)

phi = DoubleVar(root,0)
varPhi = StringVar(root,"Orientation : 0.00")
labelPhi = Label(root, textvariable = varPhi)
labelPhi.place(x=330, y=400)

############## Botones de control #############

buttonStop = Button(text="Parar",command=stop)
buttonStop.place(x=450, y=300)

buttonStart = Button(text="Iniciar",command=start)
buttonStart.place(x=500, y=300)

buttonLoad = Button(text="Cargar",command=load)
buttonLoad.place(x=550, y=300)

buttonData = Button(text="Datos",command=trayectory)
buttonData.place(x=600, y=300)

root.configure(width=950, height=700)

root.after(100,callback) #Es un método definido para todos los widgets tkinter.
root.mainloop()

