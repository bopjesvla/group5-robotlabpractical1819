import sys
from naoqi import ALProxy
from Config import Config

class SimpleEyes:
    def __init__(self):
        self.eyeProxy = ALProxy("ALLeds", Config.ROBOT_IP, Config.PORT)
    def redEyes(self):
        # Example showing how to fade the ears group to mid-intensity
        name = 'FaceLeds'
        duration = 1.0
        self.eyeProxy.fadeRGB(name, 1, 0, 0, duration)
    def blueEyes(self):
        # Example showing how to fade the ears group to mid-intensity
        name = 'FaceLeds'
        duration = 1.0
        self.eyeProxy.fadeRGB(name, 0, 0, 1, duration)
    def whiteEyes(self):
        name = 'FaceLeds'
        duration = 1.0
        self.eyeProxy.fadeRGB(name, 1, 1, 1, duration)
    def noEyes(self):
        name = 'FaceLeds'
        self.eyeProxy.fade(name, 0, 1.0)
