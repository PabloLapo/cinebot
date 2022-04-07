import math
from cmath import sqrt,exp
import numpy as np

class robotics3:

     def __init__(self):
         pass


     def valores(self,x,y,x1,y1,x2,y2,x3,y3,x4,y4,v):
          yy1=y
          yy2=y1
          yy3=y2
          yy4=y3
          yy5=y4
          y = y*sqrt(-1)
          y1 = y1*sqrt(-1)
          y2 = y2*sqrt(-1)
          y3 = y3*sqrt(-1)
          y4 = y4*sqrt(-1)
          ra = x + y
          rb = x1 + y1
          rc = x2 + y2
          rd = x3 + y3
          re = x4 + y4
          des = rb-ra
          des1= rc-rb
          des2= rd-rc
          des3= re-rd
          a = des.real
          b = des.imag
          a1= des1.real
          b1= des1.imag
          a2= des2.real
          b2= des2.imag
          a3= des3.real
          b3= des3.imag
          d=sqrt(((x1-x)**2)+(((y1.imag)-(y.imag))**2))
          d1=sqrt(((x2-x1)**2)+(((y2.imag)-(y1.imag))**2))
          d2=sqrt(((x3-x2)**2)+(((y3.imag)-(y2.imag))**2))
          d3=sqrt(((x4-x3)**2)+(((y4.imag)-(y3.imag))**2))
          t=(d.real)/(v)
          t1=(d1.real)/(v)
          t2=(d2.real)/(v)
          t3=(d3.real)/(v)
          uo=sqrt((a**2)+(b**2))
          uo1=sqrt((a1**2)+(b1**2))
          uo2=sqrt((a2**2)+(b2**2))
          uo3=sqrt((a3**2)+(b3**2))
          u=(des)/(uo)
          u1=(des1)/(uo1)
          u2=(des2)/(uo2)
          u3=(des3)/(uo3)
          a01=[]
          b01=[]
          c01=[]
          d01=[]
          ts = 0.1
          N = int(t/ts)
          N1= int((t1+t)/ts)
          N2= int((t2+t1+t)/ts)
          N3= int((t3+t2+t1+t)/ts)
          for i in range(N+1):
               ve=ra+(v*u)*i*ts
               a01.append(ve)
          for j in range(N,N1+1,1):
               ve1=rb+(v*u1)*((j-int(N))*ts)
               b01.append(ve1)
          for k in range(N1,N2+1,1):
               ve2=rc+(v*u2)*((k-int(N1))*ts)
               c01.append(ve2)
          for l in range(N2,N3+1,1):
               ve3=rd+(v*u3)*((l-int(N2))*ts)
               d01.append(ve3)
          px = [ele.real for ele in a01] + [ele.real for ele in b01] + [ele.real for ele in c01] + [ele.real for ele in d01]
          py = [ele.imag for ele in a01] + [ele.imag for ele in b01] + [ele.imag for ele in c01] + [ele.imag for ele in d01]
          data=[x,y,x1,y1,x2,y2,x3,y3,x4,y4]
          xx=[x,x1,x2,x3,x4]
          yy=[yy1,yy2,yy3,yy4,yy5]
          
          return(px,py,xx,yy)
