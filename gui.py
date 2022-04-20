"""Cinebot GUI."""
import os
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
from utils import Robot

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
        self.configureTimers()

    def configureGUI(self):
        """Configures buttons events."""
        self.robot = Robot()
        self.image = QImageLabel(self.qimage)
        self.startBtn.clicked.connect(lambda: self.robot.setMode("trajectory"))
        self.positionBtn.clicked.connect(lambda: self.robot.setMode("positionate"))
        self.chargeBtn.clicked.connect(lambda: self.robot.setMode("charge"))
        self.trajectoryBtn.clicked.connect(self.robot.updateTrajectory)
        self.stopBtn.clicked.connect(lambda: self.robot.setStop(True))

    def configureSerial(self):
        """Configures serial on/emit events."""
        self.serial.on("connection", self.serialConnectionStatus)
        self.serial.on("data", self.serialDataIncoming)

    def configureSocket(self):
        """Configures socket on/emit events."""
        self.socket.on("connection", self.socketConnectionStatus)
        self.socket.on(DATA_CLIENT_SERVER, self.setControlVariables)

    def configureTimers(self):
        """Configures some timers."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateVideo)
        self.timer.start(1000 // 15)  # 1000 // FPS

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
        # self.ledSerial.setChecked(status.get("arduino", False))
        print("serial connection:: ", status)

    def serialDataIncoming(self, data: str):
        """Read incoming data from the serial device."""
        # data = self.serial.toJson(data)
        #print("Arduino data:" ,data)
        # self.socket.on(DATA_CLIENT_SERVER, data)
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
        # read camera image
        image = self.camera["webcam"].read()
        if image is not None:
            image = image[20:455, 50:520]
            # Update robot status
            self.robot.update(image)
            variables = self.robot.getControlVariables()
            self.serial["arduino"].write(variables)

            # Display image
        self.image.setImage(image, 800, 600)

    def updateVideoPauseState(self, status: bool):
        """Update video pause status."""
        self.camera["webcam"].setPause(status)
        self.streamer.setPause(status)

    def positionateRobot(self):
        ...
    
    def stopRobot(self):
        ...

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