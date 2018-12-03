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

memory = None

    # def parrot(self):
    #
    #     # Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
    #     vocabulary = ["please", "hermione", "duck", "spinoza", "alpha", "pikachu"]
    #     self.speechProxy.setVocabulary(vocabulary, False)
    #
    #     # Start the speech recognition engine with user Test_speechProxy
    #     self.speechProxy.subscribe("Test_ASR")
    #     print 'Speech recognition engine started'
    #     time.sleep(20)
    #     self.speechProxy.unsubscribe("Test_ASR")
class SimpleSounds():
    def __init__(self, name):
        self.talkProxy = ALProxy("ALTextToSpeech", Config.ROBOT_IP, Config.PORT)
        # try:
        #     p = ALProxy(name)
        #     p.exit()
        # except:
        #     pass

        # print('exited existing proxy')

        # ALModule.__init__(self, name)
        # self.response = False
        # self.value = []
        # self.name = name
        self.response = False
        self.value = []
        self.name = name
        self.spr = ALProxy("ALSpeechRecognition", Config.ROBOT_IP, Config.PORT)
        self.spr.setVocabulary(['test', 'apple'], True)

        self.finished = True
        self.audioPlayer = ALProxy("ALAudioPlayer", Config.ROBOT_IP, Config.PORT)
        # self.soundSet = self.getParameter("SoundSet")
        # self.sounds = self.getParameter("Sounds")

        self.memory = ALProxy("ALMemory", Config.ROBOT_IP, Config.PORT)

    def checkSpeech(self):
        self.response = False
        # self.value = []
        # memory.subscribeToEvent("WordRecognized", self.name, "onDetect")
        # print self.memory.getData('LastWordRecognized')

    def onDetect(self, keyname, value, subscriber_name):
        self.response = True
        self.value = value
        print value
        memory.unsubscribeToEvent("LastWordRecognized", self.name)
        self.spr.pause(True)

    def getSpeech(self, wordlist, wordspotting):
        self.response = False
        self.value = []
        self.spr.setVocabulary(wordlist, wordspotting)

    def speak(self, word):
        self.talkProxy.say(word)

    def speakParallel(self, word):
        self.talkProxy.post.say(word)

    def playThunder(self):
        if self.soundset in self.audioPlayer.getLoadedSoundSetsList():
            print self.sounds
            sound = random.choice(self.sounds.split())
            self.audioPlayer.playSoundSetFile(self.soundset, sound)
        else:
            self.log("Soundset not installed: " + str(self.soundset))
        self.finished = True
        self.onStopped()
