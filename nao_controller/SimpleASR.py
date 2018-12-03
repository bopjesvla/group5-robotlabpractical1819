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
from naoqi import ALProxy, ALBroker, ALModule

import time
import math

memory = None
SpeechRecog = None
action_status = None

class SpeechRecog(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        am = ALProxy("ALAutonomousMoves")
        am.setExpressiveListeningEnabled(False)
        am.setBackgroundStrategy("none")
        self.subASR()

    def unsubASR(self):
        self.speechProxy.unsubscribe("Test_ASR")
        memory.unsubscribeToEvent("WordRecognized", "SpeechRecog")
        
        print('unsub ASR')

    def subASR(self):
        self.speechProxy = ALProxy("ALSpeechRecognition")
        # self.speechProxy = ALProxy("ALSpeechRecognition", Config.ROBOT_IP, Config.PORT)
        self.speechProxy.setLanguage("English")
        self.vocabulary = ['action','stop', 'NO PROBLEMO', 'BITE ME', 'HASTA LA VISTA', 'CUT']
        # self.speechProxy.setVocabulary(self.vocabulary, False)

        global memory
        memory = ALProxy("ALMemory")
        # memory = ALProxy("ALMemory", Config.ROBOT_IP, Config.PORT)
        memory.subscribeToEvent("WordRecognized", "SpeechRecog", "onTouched")
        # memory.subscribeToEvent("ALSpeechRecognition/Status", "SpeechRecog", "status")
        self.speechProxy.subscribe("Test_ASR")

    def onTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("WordRecognized", "SpeechRecog")

        try:
            print(value)
            if value[0] in self.vocabulary and value[1]>0.5:
                if value[0]=='action':
                    # self.tts.say('action receied. Lets start "come with me"')
                    global action_status
                    action_status = True
                # elif value[0]=='stop':
                #     SpeechRecog.unsubASR()
                # else:
                    # self.tts.say(value[0])
        except: 
            pass
        

        # Subscribe again to the event
        memory.subscribeToEvent("WordRecognized", "SpeechRecog", "onTouched")

    def getActionStatus(self):
        global action_status
        return action_status

    def setActionStatus(self, status=False):
        global action_status
        action_status = status

    def start(self):
        print('start')

    def done(self):
        print('done')
    
myBroker = None

def getASR():
    global myBroker
    myBroker = ALBroker("myBroker",
    "0.0.0.0",   # listen to anyone
    0,           # find a free port and use it
    Config.ROBOT_IP,          # parent broker IP
    Config.PORT)        # parent broker port

    global SpeechRecog
    SpeechRecog = SpeechRecog("SpeechRecog")
    return SpeechRecog

def stopASR():
    global SpeechRecog
    SpeechRecog.unsubASR()
    myBroker.shutdown()
    # return None