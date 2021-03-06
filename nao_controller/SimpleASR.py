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
cut_status = None

class SpeechRecog(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.name = name
        self.parrot = False
        self.cutEnable = False
        am = ALProxy("ALAutonomousMoves")
        am.setExpressiveListeningEnabled(False)
        am.setBackgroundStrategy("none")
        self.subASR()

    def unsubASR(self):
        self.speechProxy.unsubscribe("Test_ASR")
        memory.unsubscribeToEvent("WordRecognized", self.name)
        print('unsub ASR')

    def parrotOff(self):
        self.parrot = False
    
    def parrotOn(self):
        self.parrot = True
    

    def subASR(self):
        self.speechProxy = ALProxy("ALSpeechRecognition")
        self.tts = ALProxy("ALTextToSpeech")
        # self.speechProxy = ALProxy("ALSpeechRecognition", Config.ROBOT_IP, Config.PORT)
        self.speechProxy.setVisualExpression(False)
        self.speechProxy.setLanguage("English")
        # self.vocabulary = ['action', 'no problemo', 'bite me', 'hasta la vista baby', 'cut']
        self.vocabulary = ['action', 'NO PROBLEMO', 'BITE ME', 'HASTA LA VISTA BABY', 'cut']
        
        self.speechProxy.pause(True)
        self.speechProxy.setVocabulary(self.vocabulary, False)
        self.speechProxy.pause(False)

        global memory
        memory = ALProxy("ALMemory")
        # memory = ALProxy("ALMemory", Config.ROBOT_IP, Config.PORT)
        memory.subscribeToEvent("WordRecognized", self.name, "onTouched")
        # memory.subscribeToEvent("ALSpeechRecognition/Status", "SpeechRecog", "status")
        self.speechProxy.subscribe("Test_ASR")

    def onTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("WordRecognized", self.name)

        try:
            print(value)
            if value[0] in self.vocabulary:
                # self.tts.say(value[0])
            
                if value[0]=='action' and value[1]>0.45:
                    global action_status
                    action_status = True
                elif value[0]=='cut' and value[1]>0.39:
                    if self.cutEnable:
                        global cut_status
                        cut_status = True
                elif value[0]=='NO PROBLEMO' and value[1]>0.45:
                    if self.parrot:
                        self.tts.say(value[0])
                elif value[0]=='BITE ME' and value[1]>0.4:
                    if self.parrot:
                        self.tts.say(value[0])
                elif value[0]=='HASTA LA VISTA BABY' and value[1]>0.3:
                    if self.parrot:
                        self.tts.say(value[0])
                else:
                    pass

        except: 
            pass
        
        # Subscribe again to the event
        memory.subscribeToEvent("WordRecognized", self.name, "onTouched")

    def getActionStatus(self):
        global action_status
        return action_status

    def setActionStatus(self, status=False):
        global action_status
        action_status = status
    
    def getCutStatus(self):
        global cut_status
        return cut_status

    def setCutStatus(self, status=False):
        global cut_status
        cut_status = status

    def cutEnable(self):
        self.cutEnable = True
    
    def cutdisable(self):
        self.cutEnable = False
    

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