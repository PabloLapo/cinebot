import math
from cmath import sqrt,exp
import numpy as np

class robotics:

     def __init__(self):
         pass


     def valores(self,x,y,x1,y1,v):
          yy1=y
          yy2=y1
          y = y*sqrt(-1)
          y1 = y1*sqrt(-1)
          ri = x + y
          rf = x1 + y1
          des = rf-ri
          a = des.real
          b=des.imag
          d=sqrt(((x1-x)**2)+(((y1.imag)-(y.imag))**2))
          t=(d.real)/(v)
          uo=sqrt((a**2)+(b**2))
          u=(des)/(uo)
          a=[]
          ts = 0.1
          N = int(t/ts)
          for i in range(N):
               ve=ri+(v*u)*i*ts
               a.append(ve)
          px = [ele.real for ele in a]
          py = [ele.imag for ele in a]
          xx=[x,x1]
          yy=[yy1,yy2]
          return(px,py,xx,yy)
