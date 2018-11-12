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


class SimpleTouch:
    def __init__(self):
        self.touchProxy = ALProxy("ALTouch", Config.ROBOT_IP, Config.PORT)

    def getSensors(self):
        lst = self.touchProxy.getStatus()
        print lst[8][1]
        # for x in lst:
            # print x

    def getHeadTouch(self):
        lst = self.touchProxy.getStatus()
        # print lst[8][1]
        return lst[8][1]
