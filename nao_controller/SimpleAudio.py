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
from naoqi import ALProxy, ALModule

import time
import math
import re


class SimpleAudio():
    def __init__(self):
        self.aup = ALProxy("ALAudioPlayer", Config.ROBOT_IP, Config.PORT)
    
    def playThunder(self):
        fileId = self.aup.loadFile("/home/nao/thunder3.wav")
        self.aup.play(fileId)
