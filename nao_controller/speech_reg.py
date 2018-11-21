import time
from Config import Config
import sys

if Config.LINUX:
    sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % Config.LOCATION_NAOQI)
# from .nao_controller.Config import Config
# if Config.LINUX:
#     sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % Config.LOCATION_NAOQI)
import naoqi
from naoqi import ALModule, ALProxy, ALBroker
import argparse


Speecher = None
# SpeechRecognition = None
memory = None


class SpeechRecognitionModule(ALModule):
    def __init__(self, name):
        try:
            p = ALProxy(name)
            p.exit()
        except:
            pass

        print('exited existing proxy')

        ALModule.__init__(self, name)
        self.response = False
        self.value = []
        self.name = name
        self.spr = ALProxy("ALSpeechRecognition")

        global memory
        memory = ALProxy("ALMemory")
        # memory.subscribeToEvent("WordRecognized", "Speecher", "onDetect")

    def getSpeech(self, wordlist, wordspotting):
        self.response = False
        self.value = []
        self.spr.setVocabulary(wordlist, wordspotting)
        memory.subscribeToEvent("WordRecognized", self.name, "onDetect")

    def onDetect(self, keyname, value, subscriber_name):
        self.response = True
        self.value = value
        print value
        memory.unsubscribeToEvent("WordRecognized", self.name)
        self.spr.pause(True)


def main(ip, port):
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       ip,         # parent broker IP
       port)       # parent broker port

    print('broker initialized')

    global Speecher
    Speecher = SpeechRecognitionModule("SpeechRecognition")
    Speecher.getSpeech(['test', 'apple'], True)

    print('Speecher initialized')

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        # Speecher.spr.exit()
        # p = ALProxy("SpeechRecognition")
        # p.exit()
        myBroker.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=Config.ROBOT_IP,
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)
