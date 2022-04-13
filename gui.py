"""Cinebot GUI."""
import os
from pickle import TRUE
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer
from remio import Mockup
from widgets import QImageLabel
from routes import *
from settings import (
    serverSettings,
    streamSettings,
    cameraSettings,
    serialSettings,
)
from utils import*
from processing import*
ui_path = os.path.dirname(os.path.abspath(__file__))
ui_file = os.path.join(ui_path, "gui.ui")


class CustomMockup(QMainWindow, Mockup):
    """A class for manage a mockup with a local GUI."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui.ui", self)
        self.configureGUI()
        self.configureSerial()
        # self.configureSocket()

    def configureGUI(self):
        """Configures buttons events."""
        self.tracker = RobotControl()
        
        radio=10
        #Definimos los Robots con sus pocisiones Iniciales
        #self.Robot_dif=Robot(RED,0,0,pi/2,10)
        self.camera["webcam"].setProcessing(self.tracker.update)
        
        # self.camera["webcam"].setProcessing(self.robot.track)
        self.image = QImageLabel(self.qimage)
        self.positionBtn.clicked.connect(self.positionateRobot)
        self.stopBtn.clicked.connect(self.stopRobot)
        self.startBtn.clicked.connect(self.startRobot)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateVideo)
        self.timer.start(1000 // 10)  # 1000 // FPS

    def configureSerial(self):
        """Configures serial on/emit events."""
        #self.serial.on("connection", self.serialConnectionStatus)
        #self.serial.on("ports", self.serialPortsUpdate)
        #self.serial.on("data", self.serialDataIncoming)
        #self.serialPortsUpdate(self.serial.ports())
        ...

    def configureSocket(self):
        """Configures socket on/emit events."""
        self.socket.on("connection", self.socketConnectionStatus)
        self.socket.on(DATA_CLIENT_SERVER, self.setControlVariables)

    def socketConnectionStatus(self):
        """Shows the connection socket status."""
        status = self.socket.isConnected()
        self.ledSocket.setChecked(status)
        if status:
            self.socket.emit(JOIN_ROOM_CLIENT, "room-x")

    def serialPortsUpdate(self, ports: list):
        """Sends to the server the list of serial devices."""
        event = {"serial": {"ports": ports}}
        self.socket.emit(EVENT_CLIENT_SERVER, event)
        self.devices.clear()
        self.devices.addItems(ports)

    def serialConnectionStatus(self, status: dict = {"arduino": False}):
        """Sends to the server the serial devices connection status."""
        self.ledSerial.setChecked(status.get("arduino", False))

    def serialDataIncoming(self, data: str):
        """Read incoming data from the serial device."""
        #data = self.serial.toJson(data)
        #self.socket.on(DATA_CLIENT_SERVER, data)
        print("data", data)
        ...

    def setControlVariables(self, data: dict = {"arduino": {}}):
        """Writes data coming from the server to the serial device."""
        self.serial.write(message=data, asJson=True)

    def reconnectSerial(self, value: bool):
        """Updates the serial port."""
        if value:
            self.serial["arduino"].setPort(self.devices.currentText())
        else:
            self.serial["arduino"].disconnect()
        self.ledSerial.setChecked(self.serial["arduino"].isConnected())

    def reconnectSocket(self, value):
        """Updates the socketio connection."""
        if value:
            self.socket.start()
        else:
            self.socket.stop()
        self.ledSocket.setChecked(self.socket.isConnected())

    def updateVideo(self):
        """Updates video image."""
        image = self.camera["webcam"].read()
        self.tracker.run(image)
#         if self.tracker.isPosition():
#             uRef, wRef = self.tracker.getVariables()
#             print(wRef)
# #            self.serial["arduino"].write("Soy Python")
#         elif self.tracker.isRunnig():
#             uRef, wRef = self.tracker.getVariables()
#             print(wRef)
# #            self.serial["arduino"].write("Soy Python")
#         else:
        uRef, wRef = self.tracker.getVariables()
        #print(f"{uRef},{wRef}")
        self.serial["arduino"].write(f"{uRef},{wRef}")
        self.image.setImage(image, 400, 300)
    
    def updateVideoPauseState(self, status: bool):
        """Update video pause status."""
        self.camera["webcam"].setPause(status)
        self.streamer.setPause(status)

    def positionateRobot(self):
        self.tracker.setPosition(True)
        
    
    def stopRobot(self):
        self.tracker.setRunning(False)
        self.tracker.setPosition(False)
        
    def startRobot(self):
        self.tracker.setRunning(True)

    def closeEvent(self, e):
        """Stops running threads/processes when close the windows."""
        self.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    experiment = CustomMockup(
        serverSettings=serverSettings,
        streamSettings=streamSettings,
        cameraSettings=cameraSettings,
        serialSettings=serialSettings,
    )
    experiment.start(camera=True, serial=True, socket=False, streamer=False, wait=False)
    experiment.show()
    sys.exit(app.exec_())

