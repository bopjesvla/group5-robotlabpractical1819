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
        # self.aup = ALProxy("ALSoundPlayback", Config.ROBOT_IP, Config.PORT)

     
    # def playThunder(self):
    #     if self.soundset in self.audioPlayer.getLoadedSoundSetsList():
    #         print self.sounds
    #         sound = random.choice(self.sounds.split())
    #         self.audioPlayer.playSoundSetFile(self.soundset, sound)
    #     else:
    #         self.log("Soundset not installed: " + str(self.soundset))
    #     self.finished = True
    #     self.onStopped()
    
    def playThunder(self):
        # print "thunder"
        # fileId = 
        # self.aup.playFile("C:/Users/Sameera/Downloads/thunder3.wav")
        # time.sleep(5)
        # fileId = self.aup.post.playFile("C:/Users/Sameera/Downloads/thunder3.wav")
        # self.aup.playWavFile("C:/Users/Sameera/Downloads/thunder3.wav")
        # self.aup.play(fileId)

        fileId = self.aup.loadFile("C:/Users/Sameera/Downloads/thunder3.wav")
        self.aup.play(fileId)
        # self.aup.play(fileId, _async=True)
        
        time.sleep(3)
        print 'sdfdf'
