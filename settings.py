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

cameraSettings = {
    "webcam": {
        "src": 1,
        "fps": None,
        "size": None,
        "flipX": False,
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
        "port": "COM6",
        "baudrate": 9600,
        "timeout": 1.0,
        "reconnectDelay": 5,
        "portsRefreshTime": 5,
        "emitterIsEnabled": True,
    },
}