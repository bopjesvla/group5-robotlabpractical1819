import sys
from Config import Config

if Config.LINUX:
    sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % Config.LOCATION_NAOQI)

from naoqi import ALProxy

class SimpleTracker:
    def __init__(self):
        self.trackProxy = ALProxy("ALTracker", Config.ROBOT_IP, Config.PORT)
    def face(self):
        self.trackProxy.registerTarget("Face", 100)
        self.trackProxy.track("Face")
        pos = firstPos = self.trackProxy.getTargetPosition()
        print firstPos

        while len(pos) <= len(firstPos) and sum(abs(old - new) for old, new in zip(pos, firstPos)) < 3:
            pos = self.trackProxy.getTargetPosition()
    def unface(self):
        self.trackProxy.stopTracker()
        self.trackProxy.unregisterTarget('Face')
        self.trackProxy.setEffector("None")

