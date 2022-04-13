"""Settings file."""
from decouple import AutoConfig

from routes import *

# ENV PATH
config = AutoConfig(search_path="./.env")

# ------------------------ SERVER SETTINGS ------------------------------------

serverSettings = {
    "address": config("address", default="http://localhost:3000", cast=str),
    "request_timeout": 10,
}
# ------------------------- STREAM SETTINGS -----------------------------------

streamSettings = {
    "endpoint": STREAM_CLIENT_SERVER,
    "quality": 30,
    "fps": 10,
    "colorspace": "bgr",
    "colorsubsampling": "422",
    "fastdct": True,
    "enabled": True,
}

# ------------------------- CAMERA SETTINGS ------------------------------------
#[600, 400]
cameraSettings = {
    "webcam": {
        "src": 0,
        "fps": None,
        "size": None,
        "flipX": True,
        "flipY": False,
        "emitterIsEnabled": False,
        "backgroundIsEnabled": True,
        "processing": None,
        "processingParams": {},
        "encoderIsEnable": False,
    },
}

# --------------------------- SERIAL SETTINGS ------------------------------

serialSettings = {
    "arduino": {
        "port": 'COM4',
        "baudrate": 9600,
        "timeout": 1.0,
        "reconnectDelay": 5,
        "portsRefreshTime": 5,
        "emitterIsEnabled": True,
    },
}