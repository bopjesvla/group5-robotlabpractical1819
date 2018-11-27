import sys
from Config import Config

if Config.LINUX:
    sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % Config.LOCATION_NAOQI)

from naoqi import ALProxy

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
