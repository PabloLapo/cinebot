from trayectory import *
import random
  

def inicial(largo,alto,distanciaX,distanciaY,xo1,yo1,xo2,yo2,
            xo3,yo3,xo4,yo4,
            xo5,yo5,xo6,yo6,
            xo7,yo7,xo8,yo8,xo9,yo9):
    ### ORIGEN ALETARORIO##
    tyO1=ori(xo1,yo1)
    ###
    tyO2=ori(xo2,yo2)
    ###
    tyO3=ori(xo3,yo3)
    ###
    tyO4=ori(xo4,yo4)
    ###
    tyO5=ori(xo5,yo5)
    ###
    tyO6=ori(xo6,yo6)
    ####
    tyO7=ori(xo7,yo7)
    ###
    tyO8=ori(xo8,yo8)
    ###
    tyO9=ori(xo9,yo9)
    ####fin coordenadas de origen###
    valores_o=[tyO1,tyO2,tyO3,tyO4,tyO5,tyO6,tyO7,tyO8,tyO9]
    data_o=random.choice(valores_o)
    hxo=data_o[0]
    hyo=data_o[1]
    if len(hxo) > 1:
        hxdo = []
        hydo = []
        for i in range(len(hxo)):
            hxdo.append(int(hxo[i]*largo/distanciaX))
            hydo.append(int(hyo[i]*alto/distanciaY))
    return(hxdo,hydo)            
def trayectory(largo,alto,distanciaX,distanciaY,
               xTy1p1,yTy1p1,xTy1p2,yTy1p2,xTy1p3,yTy1p3,xTy1p4,yTy1p4,
               xTy2p1,yTy2p1,xTy2p2,yTy2p2,xTy2p3,yTy2p3,xTy2p4,yTy2p4,
               xTy3p1,yTy3p1,xTy3p2,yTy3p2,xTy3p3,yTy3p3,xTy3p4,yTy3p4,
               xTy4p1,yTy4p1,xTy4p2,yTy4p2,xTy4p3,yTy4p3,xTy4p4,yTy4p4,
               xTy5p1,yTy5p1,xTy5p2,yTy5p2,xTy5p3,yTy5p3,xTy5p4,yTy5p4):
    k = 0
##    ###tray1ectoria 8###
    ty101=cuatro(xTy1p1,yTy1p1,xTy1p2,yTy1p2,xTy1p3,yTy1p3,xTy1p4,yTy1p4)
##    ###trayectoria 9###
    ty102=cuatro(xTy2p1,yTy2p1,xTy2p2,yTy2p2,xTy2p3,yTy2p3,xTy2p4,yTy2p4)
#####trayectoria 16###
    ty103=cuatro(xTy3p1,yTy3p1,xTy3p2,yTy3p2,xTy3p3,yTy3p3,xTy3p4,yTy3p4)
#####trayectoria 17###
    ty104=cuatro(xTy4p1,yTy4p1,xTy4p2,yTy4p2,xTy4p3,yTy4p3,xTy4p4,yTy4p4)
#####trayectoria 5###
    ty105=cuatro(xTy5p1,yTy5p1,xTy5p2,yTy5p2,xTy5p3,yTy5p3,xTy5p4,yTy5p4)
#############################
    valores=[ty101,ty102,ty103,ty104,ty105]
    data=random.choice(valores)
    ###
    hxdm=ty101[0]
    hydm=ty101[1]
    if len(hxdm) > 1:
        hxd = []
        hyd = []
        for i in range(len(hxdm)):
            hxd.append(int(hxdm[i]*largo/distanciaX))
            hyd.append(int(hydm[i]*alto/distanciaY))
    return(hxd,hyd,k)
def load(posicionRobotX,posicionRobotY,posicionCargaX,posicionCargaY):
    k = 0
    data=cuatro(posicionRobotX,posicionRobotY,posicionCargaX,posicionCargaY)
    hxdm=data[0]
    hydm=data[1]
    if len(hxdm) > 1:
        hxd = []
        hyd = []
        for i in range(len(hxdm)):
            hxd.append(int(hxdm[i]*largo/distancia_x))
            hyd.append(int(hydm[i]*alto/distancia_y))
    return(hxd,hyd,k)
### trayextoria tres puntos ###
def ori(x,y):
    val = robotics()
    yy=val.origen(x,y)
    return (yy[0],yy[1])
def tres(x,y,x1,y1,x2,y2):
    v=0.1
    val = robotics()
    yy=val.valores_2(x,y,x1,y1,x2,y2)
    return (yy[0],yy[1])

### trayextoria cuatro puntos ###
def cuatro(x,y,x1,y1,x2,y2,x3,y3):
    val2 = robotics()
    yy=val2.valores_3(x,y,x1,y1,x2,y2,x3,y3)
    return (yy[0],yy[1])
### trayextoria cinco puntos ###
def cinco(x,y,x1,y1,x2,y2,x3,y3,x4,y4):
    val3 = robotics()
    yy=val3.valores_4(x,y,x1,y1,x2,y2,x3,y3,x4,y4)
    return (yy[0],yy[1])
