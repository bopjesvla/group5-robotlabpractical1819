import numpy as np
import time
from Tkinter import *
from PIL import Image, ImageTk
from Config import Config
from SimpleMotions import SimpleMotions
from SimpleVisions import SimpleVisions
from SimpleSounds import SimpleSounds
from SimpleTracker import SimpleTracker
from SimpleEyes import SimpleEyes
from SimpleTouch import SimpleTouch
from SimpleAudio import SimpleAudio
from SimpleASR import getASR, stopASR

if Config.LINUX:
    sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % Config.LOCATION_NAOQI)

debug = False
SpeechRecog = None
lastStage = False

# if not debug:
motionObj = SimpleMotions()
visionObj = SimpleVisions()
soundObj = SimpleSounds("SpeechRecognition")
eyesObj = SimpleEyes()
trackObj = SimpleTracker()
audioObj = SimpleAudio()
touchObj = SimpleTouch()


def comeWithMe():
    print 'comeWithMe'
    # brigit - Come with me 1, 3, 5, 7

    # 1. Eyes RED
    eyesObj.redEyes()

    # 2. Terminator vision turns on, specifications like last time,
    # so with bounding boxes around the face, etc.
    # 3. Nao walks toward the human actor sitting on the floor.
    # Nao stops close to the actor. Make sure the Nao doesn't bump into the actor.

    # 2 and 3
    visionObj.faceFollow(motionObj, soundObj, stopDist=80)

    # 4. When a face is located, the Text on the terminator vision should be HELP.

    # 5. Nao goes into a crouching position, facing the human, see Figure 1.
    motionObj.CrouchWhileSpeaking()
    # 6. At the same time the Nao says COME WITH ME IF YOU WANT TO LIVE. = Sameera
    # See the python files in the Gitlab repo for examples of running parallel processes on the Nao.
    # soundObj.speakParallel("COME WITH ME IF YOU WANT TO LIVE")
    soundObj.speak("COME WITH Me IF YOU WANT TO Liv")

    # 7. The Nao goes back into standing position and walks 2 meters in a random direction.

    motionObj.stand()

    rot = np.random.choice([140,160,180,-140,-160,-180])
    # rot = 110
    motionObj.rotateTheta(rot)

    motionObj.moveXYCm(60, 0)

    # 8. The Nao turns around and looks at the actor.
    # use turn angles from (7) to turn the head - so Nao will directly look at the actor

    motionObj.rotateTheta(180)

    trackObj.face()

    # 9. The Nao does a 'come here' gesture with its arm, while saying COME HERE SARAH CONNOR, NAO!. = Sameera
    soundObj.speakParallel("COME HERE SARAH CONNOR, NAO!")
    motionObj.gestureCome() # uncomment

    trackObj.unface()

    # 10. The actor stands up and walks towards the Nao
    pass

def hastaLaVistaPre():
    print 'hastaLaVistaPre'
    # brigit - Hasta la vista 1,2
    # 1. While the actor is walking towards the Nao, the Nao sits down.
    motionObj.sit()
    eyesObj.greenEyes()
    # 2. The Nao eye LEDs turn green.
    # pass

def hastaLaVista():
    # print 'HastaLaVista'

    # 3. The terminator vision gets a green overlay.
    visionObj.terminator(color='green')

    # 4. The actor sits down facing the Nao.

    # 5. The actor touches the Nao's head sensor, the Nao says AFFIRMATIVE, enters parrot mode. - Sameera
    # 6. Actor says NO PROBLEMO, Nao repeats.
    # 7. Actor says BITE ME, Nao repeats.
    # 8. Actor says HASTA LA VISTA BABY, Nao repeats.
    # 9. Actor touches Nao's head, Nao exits parrot mode and says TALK TO THE HAND.
    letsParrot()

    pass

def letsParrot():
    if touchObj.w5HastaLaVista_T5(soundObj) == True:
        SpeechRecog.parrotOn()
        print 'parrot ON'
    elif touchObj.w5HastaLaVista_T5(soundObj) == False:
        SpeechRecog.parrotOff()
        print 'parrot OFF'
        global lastStage
        lastStage = True
        SpeechRecog.cutEnable()
    else:
        pass

SpeechRecog = getASR()

def main():
    """ Main entry point
    """
    motionObj.stand()

    try:
        global SpeechRecog
        global lastStage
        SpeechRecog.subASR()
        n = 0
        hastaEn = False
        lastStage = False

        while True:
            asrST = SpeechRecog.getActionStatus()
            
            if asrST:
                SpeechRecog.setActionStatus(False)
                comeWithMe()
                hastaLaVistaPre()
                hastaEn = True
                asrST = False
                
            if hastaEn:
                hastaLaVista()
            
            if lastStage:
                asrCut = SpeechRecog.getCutStatus()
                # 10. When the director Nao hears this, it says CUT!.
                # 11. The Nao stands up and walks to the middle of the room.
                if asrCut:
                    SpeechRecog.setCutStatus(False)
                    motionObj.stand(0.4)
                    motionObj.rotateTheta(140)
                    motionObj.moveXYCm(120, 0)
                    motionObj.Crouch()

    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        # SpeechRecog.unsubASR()
        # if SpeechRecog != None:
        stopASR()
        sys.exit(0)

if __name__ == "__main__":
    main()
    motionObj.rest()
