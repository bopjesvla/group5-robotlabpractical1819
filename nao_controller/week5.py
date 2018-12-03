import numpy as np
import time
from Tkinter import *
from PIL import Image, ImageTk
from Config import Config
from SimpleMotions import SimpleMotions
from SimpleVisions import SimpleVisions
from SimpleSounds import SimpleSounds
from SimpleEyes import SimpleEyes
from SimpleTouch import SimpleTouch
from SimpleAudio import SimpleAudio
from SimpleASR import SimpleASR, SpeechRecog, getASR, stopASR

if Config.LINUX:
    sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % Config.LOCATION_NAOQI)

debug = False
SpeechRecog = None
# global SpeechRecog
    
if not debug:
    motionObj = SimpleMotions()
    visionObj = SimpleVisions()
    soundObj = SimpleSounds("SpeechRecognition")
    # soundObj.getSpeech(['test', 'apple'], True)
    eyesObj = SimpleEyes()
    audioObj = SimpleAudio()
    touchObj = SimpleTouch()
    # asrObj = SimpleASR()
    # SpeechRecog = SpeechRecog("SpeechRecog")
    SpeechRecog = getASR()

def main():
    """ Main entry point
    """

    try:
        SpeechRecog.subASR()
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        # SpeechRecog.unsubASR()
        stopASR()
        sys.exit(0)

if __name__ == "__main__":
    main()