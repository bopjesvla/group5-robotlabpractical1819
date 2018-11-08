'''
This is the basic tutorial, showing how to do some basic things with the Nao
* sonar
To stop this program, do a keyboard interrupt in your shell (Ctrl+C)
'''

from naoqi_hacky.naoqi import ALProxy, ALModule, ALBroker
import time
import argparse

IP = "192.168.1.105"
PORT = 9559

global mst, tts

class SonarTut(ALModule):
    def __init__(self, strName):
        try:
            p = ALProxy(strName)
            p.exit()
        except:
            pass
        self.front = False
        ALModule.__init__( self, strName );
        self.memory = ALProxy("ALMemory")
        sonard = ALProxy("ALSonar")
        sonard.subscribe("SonarTut")
        self.memory.subscribeToEvent("SonarLeftDetected", strName, "sonarLeft")
        self.memory.subscribeToEvent("SonarRightDetected", strName, "sonarRight")

    def sonarLeft(self, key, value, message):
        print "I sense left"
        tts.say("I sense left")
        

    def sonarRight(self, key, value, message):
        print "I sense right"
        tts.say("I sense right")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip",
                      help="IP adress of the robot",
                      dest="IP",
                      default=IP)

    parser.add_argument("--pport",
                      help="Port of communication with the robot",
                      dest="PORT",
                      default=9559)

    parser.add_argument("--rate",
                    help="Sampling rate",
                    dest="rate",
                    default=48000)

    args=parser.parse_args()
    args.rate = int(args.rate)
    args.PORT = int(args.PORT)
    pythonBroker = ALBroker("pythonBroker", "0.0.0.0", 9600, args.IP, args.PORT)
    sonars = SonarTut("sonars")
    pst = ALProxy("ALRobotPosture")
    tts = ALProxy("ALTextToSpeech")
    mst = ALProxy("ALMotion")

    mst.wakeUp()
    pst.goToPosture("Crouch", 1.0)
    mst.rest()

    try:
        while True:
            time.sleep(1)

    except:
        pst.goToPosture('Sit', 0.5)
        mst.rest()
        pythonBroker.shutDown()
