'''
http://doc.aldebaran.com/2-1/naoqi/sensors/altouch.html
This is the basic tutorial, showing how to do some basic things with the Nao
* tactile buttons
Job's hand sensors seem insensitive and could not be reliably activated during
our own testing.
'''

from naoqi import ALProxy, ALBroker, ALModule
import sys
import time
import argparse

# Global variable to store the ReactToTouch module instance
ReactToTouch = None

memory = None
SpeechRecog = None

class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to TouchChanged event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("TouchChanged",
            "ReactToTouch",
            "onTouched")

    def onTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("TouchChanged",
            "ReactToTouch")

        touched_bodies = []
        for p in value:
            if p[1]:
                touched_bodies.append(p[0])
        print(touched_bodies)
        # self.say(touched_bodies)

        # Subscribe again to the event
        memory.subscribeToEvent("TouchChanged",
            "ReactToTouch",
            "onTouched")

    def say(self, bodies):
        if (bodies == []):
            return

        sentence = "My " + bodies[0]

        for b in bodies[1:]:
            sentence = sentence + " and my " + b

        if (len(bodies) > 1):
            sentence = sentence + " are"
        else:
            sentence = sentence + " is"
        sentence = sentence + " touched."

        self.tts.say(sentence)

class SpeechRecog(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")
        
        # self.speechProxy.unsubscribe("Test_ASR")
        
        self.subASR()

        # Subscribe to TouchChanged event:
        # global memory
        # memory = ALProxy("ALMemory")
        # memory.subscribeToEvent("WordRecognized", "SpeechRecog", "onTouched")

        # self.speechProxy.subscribe("Test_ASR")
        # time.sleep(20)
        # self.speechProxy.unsubscribe("Test_ASR")

    def unsubASR(self):
        self.speechProxy.unsubscribe("Test_ASR")
        memory.unsubscribeToEvent("WordRecognized", "SpeechRecog")
        print('unsub ASR')

    def subASR(self):
        self.speechProxy = ALProxy("ALSpeechRecognition")
        self.speechProxy.setLanguage("English")
        self.vocabulary = ['action','stop', 'NO PROBLEMO', 'BITE ME', 'HASTA LA VISTA', 'CUT']
        # self.speechProxy.setVocabulary(self.vocabulary, False)

        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("WordRecognized", "SpeechRecog", "onTouched")
        # memory.subscribeToEvent("ALSpeechRecognition/Status", "SpeechRecog", "status")
        self.speechProxy.subscribe("Test_ASR")

    def status(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("ALSpeechRecognition/Status", "SpeechRecog")

        print(value)
        

        # Subscribe again to the event
        memory.subscribeToEvent("ALSpeechRecognition/Status", "SpeechRecog", "status")

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
                    self.tts.say('action receied. Lets start "come with me"')
                # elif value[0]=='stop':
                #     SpeechRecog.unsubASR()
                else:
                    self.tts.say(value[0])
        except: 
            pass
        

        # Subscribe again to the event
        memory.subscribeToEvent("WordRecognized", "SpeechRecog", "onTouched")

    def start(self):
        print('start')

    def done(self):
        print('done')

    

def main(ip, port):
    """ Main entry point
    """
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exits
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       ip,          # parent broker IP
       port)        # parent broker port


    # global ReactToTouch
    # ReactToTouch = ReactToTouch("ReactToTouch")
    global SpeechRecog
    SpeechRecog = SpeechRecog("SpeechRecog")

    try:
        # while True:
        #     time.sleep(1)
        t = 1
        SpeechRecog.start()
        while t < 20:
            time.sleep(1)
            t += 1
            print t
        SpeechRecog.unsubASR()
        myBroker.shutdown()
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        SpeechRecog.unsubASR()
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default='192.168.1.103',
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)
