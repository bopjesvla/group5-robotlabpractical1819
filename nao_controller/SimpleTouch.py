'''
======================================================================================================
 https://github.com/redsphinx/Simple-NAO-Controller
 Written by Gabrielle Ras
 12 September 2014 
 version 1.1

 This is the SimpleSounds module. Everything that has to so with the speakers of the NAO will be here. 

 This module allows you to make the NAO:
 - Speak

 The required software version is naoqi 2.1
======================================================================================================
'''


from Config import Config
import sys

if Config.LINUX:
    sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % Config.LOCATION_NAOQI)

import naoqi
import almath
from naoqi import ALProxy

import time
import math
import re

touchStatus = False
preTouchStatus = False
count = 0

class SimpleTouch:
    def __init__(self):
        self.touchProxy = ALProxy("ALTouch", Config.ROBOT_IP, Config.PORT)

    def getSensors(self):
        lst = self.touchProxy.getStatus()
        # print status of all sensors
        print lst[8][1]

    def getHeadTouch(self):
        lst = self.touchProxy.getStatus()
        # return the status of 'head/touch/middle' sensor
        return lst[8][1]

    def oof(self):
        # HeadTouch = False
        lst = self.touchProxy.getStatus()
        if any('Head' in name and s for name, s, _ in lst):
            return "ouch"
        if any('Foot' in name and s for name, s, _ in lst):
            return "oof"
        # if any('Hand' in name and s for name, s, _ in lst):
        #     return 'reset'

    def task3(self, soundObj, motionObj):
        global touchStatus
        global preTouchStatus
        touchStatus = self.getHeadTouch()
        if(touchStatus == True and preTouchStatus == False):
            preTouchStatus = True
        elif(touchStatus == False and preTouchStatus == True):
            preTouchStatus = False
            global count
            count += 1
            if(count%2==1):
                soundObj.speak("I'm going to Sit")
                motionObj.sit()
            else:
                soundObj.speak("I'm going to Stand")
                motionObj.stand()
        else:
            pass
