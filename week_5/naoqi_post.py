"""
In this tutorial I will show you how to make the Nao move, speak and change eye color at the same time
You DO need a Nao for this part
"""
import sys
from config import LINUX, IP, PORT, LOCATION_NAOQI
from util import init_leds, eyes_rgb

if LINUX:
    sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % LOCATION_NAOQI)

from naoqi import ALProxy

motion_proxy = ALProxy('ALMotion', IP, PORT)
speech_proxy = ALProxy('ALTextToSpeech', IP, PORT)
led_proxy = ALProxy('ALLeds', IP, PORT)
postureProxy = ALProxy('ALRobotPosture', IP, PORT)

init_leds(led_proxy)
postureProxy.goToPosture("Stand", 0.6667)
motion_proxy.moveInit()

# Every proxy you create has an attribute named 'post' that you can use to call long methods in the background.
motion_proxy.post.moveTo(0.5, 0, 0)  # will walk ~50 cm forward
speech_proxy.post.say('lalalalalalalalalala, lalalalalallalala, lalalalaalala')
eyes_rgb(led_proxy)
postureProxy.goToPosture('Sit', 0.6667)
motion_proxy.rest()
