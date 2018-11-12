'''
This is the basic tutorial, showing how to do some basic things with the Nao
* speech
'''
import sys
MY_LOCATION = open('../LOCATION').read()
sys.path.append(MY_LOCATION)
import naoqi

# --------------------------------------------------------------------------------------
# Initialize proxies
# --------------------------------------------------------------------------------------
ip = 'localhost'
port = 9559
tts = naoqi.ALProxy('ALTextToSpeech', ip, port)


# --------------------------------------------------------------------------------------
# Speech: make the Nao say something
# --------------------------------------------------------------------------------------
def speak(something='hello world'):
    tts.say(something)


# --------------------------------------------------------------------------------------
# Speech: set the speech volume
# --------------------------------------------------------------------------------------
def set_volume(vol):
    print('current volume at %f' % tts.getVolume())
    if 0.0 <= vol <= 1.0:
        tts.setVolume(vol)
    else:
        print('volume level %f not valid' % vol)


# --------------------------------------------------------------------------------------
# Speech: get the language setting
# --------------------------------------------------------------------------------------
def get_language():
    print(tts.getLanguage())

# --------------------------------------------------------------------------------------
# Run above functions for tests:
# ------------------------------------------------------------------------------
speak()
get_language()
set_volume(0.1)
speak("I am being very quiet.")
set_volume(1)
speak("I am being very loud.")
