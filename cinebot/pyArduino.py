from threading import Thread
import serial
import time
import sys


class serialArduino:
     def __init__(self,port,baud=9600,sizeData=1):
          self.port = port
          self.baud = baud
          self.sizeData = sizeData 

          self.isReceiving = False
          self.isRun     = True
          self.thread    = None
          
          self.rawData = [None]*self.sizeData
          print('Trying to connect to: ' + str(self.port))
          try:
               self.serialConnection = serial.Serial(self.port,self.baud)
               print('Connected to ' + str(self.port))
          except:
               sys.exit("Failed to connect with " + str(self.port))
               
     def readSerialStart(self):
          if self.thread == None:
               self.thread = Thread(target=self.backgroundThread)
               self.thread.start()
               while self.isReceiving != True:
                    print("Starting receive data")
                    time.sleep(0.1)
               print("Receiving Data")
                    
     def backgroundThread(self):
          time.sleep(1.0)
          self.serialConnection.flushInput()
          while (self.isRun):
               for k in range(self.sizeData):
                    try:
                         self.rawData[k] = float(self.serialConnection.readline().strip())
                    except:
                         sys.exit("Error data receive")
               self.isReceiving = True
               
     def sendData(self,dataToSend,separator=','):
          stringData = ""
          sizeSendData = len(dataToSend)
          #dataToSend = lista[]
          for k in range(sizeSendData):
               if k < sizeSendData-1:
                    stringData = stringData+str(dataToSend[k])+','
               else:
                    stringData = stringData+str(dataToSend[k])
          
          self.serialConnection.write((stringData+'\n').encode())     
               
          
     def close(self):
          self.isRun = False
          if self.thread == None:
               pass
          else:
               self.thread.join()
          self.serialConnection.close()
          print('Serial Port Disconnected...')
          













