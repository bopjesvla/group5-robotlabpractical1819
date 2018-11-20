'''
======================================================================================================
 https://github.com/redsphinx/Simple-NAO-Controller
 Written by Gabrielle Ras
 12 September 2014 
 version 1.1

 This is the SimpleVisions module. Everything that has to do with the camera of the NAO will be here.

 This module allows you to make the NAO:
 - Take a picture

 The required software version is naoqi 2.1
 =====================================================================================================
'''

from Config import Config
import sys

if Config.LINUX:
    sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % Config.LOCATION_NAOQI)

import naoqi
import cv2
import almath
import vision_definitions
from naoqi import ALProxy
import face_recognition

import time
# import Image
from PIL import Image
import math
import numpy as np
from SimpleMotions import SimpleMotions

#global visionProxy
#resolution = 2    # VGA
resolution = vision_definitions.kVGA#kVGA #kQVGA  # QQVGA (160 * 120)
colorSpace = 11   # RGB
#colorSpace = vision_definitions. nt sure whats happening here
motionObj = SimpleMotions()

class SimpleVisions:
    def __init__(self):
        self.visionProxy = ALProxy("ALVideoDevice", Config.ROBOT_IP, Config.PORT)
        self.motionProxy = ALProxy("ALMotion", Config.ROBOT_IP, Config.PORT)

        pass

    def terminator(self):
        #motionObj.moveHeadPitch(0.3, 0.4)
        #time.sleep(2)
        videoClient = self.visionProxy.subscribeCamera("python_client", 0, resolution, colorSpace, 5)
        self.visionProxy.setCameraParameter(videoClient, 18, 0)
        picture = self.visionProxy.getImageRemote(videoClient)
        #picture2 = self.visionProxy.getImageLocal(videoClient)
        self.visionProxy.unsubscribe(videoClient)
        picWidth = picture[0]
        picHeight = picture[1]
        array = picture[6]
        realPicture = Image.frombytes("RGB", (picWidth, picHeight), array)
        m = np.array(realPicture)
        loc = face_recognition.face_locations(m)
        if loc:
            print loc
            realPicture.save("analyzeThis.png", "PNG")
            t, r, b, l = loc[0]
            m[t:b,l-1:l+1,:] = 255
            m[t:b,r-1:r+1,:] = 255
            m[t-1:t+1,l:r,:] = 255
            m[b-1:b+1,l:r,:] = 255
            realPicture = Image.fromarray(m)

        r, g, b = realPicture.split()
        r = r.point(lambda i: i * 1.5)
        g = g.point(lambda i: i / 1.5)
        b = b.point(lambda i: i / 1.5)
        realPicture = Image.merge('RGB', (r,g,b))
        realPicture.save("terminated.png", "PNG")

        # realPicture.show()

        return loc
