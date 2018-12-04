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
    
# if not debug:
motionObj = SimpleMotions()
visionObj = SimpleVisions()
soundObj = SimpleSounds("SpeechRecognition")
eyesObj = SimpleEyes()
trackObj = SimpleTracker()
audioObj = SimpleAudio()
touchObj = SimpleTouch()
SpeechRecog = getASR()

def comeWithMe():
    print 'comeWithMe'
    # brigit - Come with me 1, 3, 5, 7

    # 1. Eyes RED

    # 2. Terminator vision turns on, specications like last time, 
    # so with bounding boxes around the face, etc.
    
    # 3. Nao walks toward the human actor sitting on the floor. 
    # Nao stops close to the actor. Make sure the Nao doesn't bump into the actor.

    # 4. When a face is located, the Text on the terminator vision should be HELP.

    # 5. Nao goes into a crouching position, facing the human, see Figure 1.

    # 6. At the same time the Nao says COME WITH ME IF YOU WANT TO LIVE. = Sameera
    # See the python files in the Gitlab repo for examples of running parallel processes on the Nao.
    soundObj.speakParallel("COME WITH ME IF YOU WANT TO LIVE")

    # 7. The Nao goes back into standing position and walks 2 meters in a random direction.

    motionObj.stand()

    rot = np.random.choice([120,140,160,180,-120,-140,-160,-180])
    motionObj.rotateTheta(rot)

    motionObj.moveXYCm(120, 0)

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

def hastaLaVista():
    print 'HastaLaVista'
    # brigit - Hasta la vista 1,2

    # 1. While the actor is walking towards the Nao, the Nao sits down.

    # 2. The Nao eye LEDs turn green.

    # 3. The terminator vision gets a green overlay.

    # 4. The actor sits down facing the Nao.

    # 5. The actor touches the Nao's head sensor, the Nao says AFFIRMATIVE, enters parrot mode.
    '''says AFFIRMATIVE > implemented in the passive loop '''
    # 6. Actor says NO PROBLEMO, Nao repeats.

    # 7. Actor says BITE ME, Nao repeats.

    # 8. Actor says HASTA LA VISTA BABY, Nao repeats.

    # 9. Actor touches Nao's head, Nao exits parrot mode and says TALK TO THE HAND.

    # 10. When the director Nao hears this, it says CUT!.

    # 11. The Nao stands up and walks to the middle of the room.

    pass

def main():
    """ Main entry point
    """
    motionObj.stand()
    try:
        
        SpeechRecog.subASR()
        while True:
            time.sleep(1)
            asrST = SpeechRecog.getActionStatus()
            if asrST:
                # soundObj.speak("start Come with me")
                SpeechRecog.setActionStatus(False)
                stopASR()
                # SpeechRecog = None
                comeWithMe()
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        # SpeechRecog.unsubASR()
        # if SpeechRecog != None:
        #     stopASR()
        sys.exit(0)

if __name__ == "__main__":
    main()
    motionObj.rest()
