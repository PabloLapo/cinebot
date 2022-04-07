import math
from cmath import sqrt,exp
import numpy as np

class robotics1:

     def __init__(self):
         pass


     def valores(self,x,y,x1,y1,x2,y2,v):
          yy1=y
          yy2=y1
          yy3=y2
          y = y*sqrt(-1)
          y1 = y1*sqrt(-1)
          y2 = y2*sqrt(-1)
          ra = x + y
          rb = x1 + y1
          rc = x2 + y2
          des = rb-ra
          des1= rc-rb
          a = des.real
          b = des.imag
          a1= des1.real
          b1= des1.imag
          d=sqrt(((x1-x)**2)+(((y1.imag)-(y.imag))**2))
          d1=sqrt(((x2-x1)**2)+(((y2.imag)-(y1.imag))**2))
          t=(d.real)/(v)
          t1=(d1.real)/(v)
          uo=sqrt((a**2)+(b**2))
          uo1=sqrt((a1**2)+(b1**2))
          u=(des)/(uo)
          u1=(des1)/(uo1)
          a=[]
          b=[]
          ts = 0.1
          N = int(t/ts)
          N1= int((t1+t)/ts)
          for i in range(N+1):
               ve=ra+(v*u)*i*ts
               a.append(ve)
          for j in range(N,N1+1,1):
               ve1=rb+(v*u1)*((j-int(N))*ts)
               b.append(ve1)
          px = [ele.real for ele in a]+[ele.real for ele in b]
          py = [ele.imag for ele in a]+[ele.imag for ele in b]
          data=[x,y,x1,y1,x2,y2]
          xx=[x,x1,x2]
          yy=[yy1,yy2,yy3]
          return(px,py,xx,yy)
