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
        print "picture taken"
        #picture2 = self.visionProxy.getImageLocal(videoClient)
        self.visionProxy.unsubscribe(videoClient)
        picWidth = picture[0]
        picHeight = picture[1]
        array = picture[6]
        realPicture = Image.frombytes("RGB", (picWidth, picHeight), array)
        m = np.array(realPicture)
        haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = haar_face_cascade.detectMultiScale(m, minNeighbors=5)
        print faces
        if len(faces)>0:
            (l, t, w, h) = faces[0]
            r = l + w
            b = t + h
            realPicture.save("analyzeThis.png", "PNG")
            m[t:b,l-1:l+1,:] = 255
            m[t:b,r-1:r+1,:] = 255
            m[t-1:t+1,l:r,:] = 255
            m[b-1:b+1,l:r,:] = 255
            realPicture = Image.fromarray(m)

            from PIL import ImageFont
            from PIL import ImageDraw

            draw = ImageDraw.Draw(realPicture)
            # font = ImageFont.truetype(<font-file>, <font-size>)
            # draw.text((x, y),"Sample Text",(r,g,b))
            text = 't: {}\nb: {}\nr: {}\nl: {}'.format(t, b, r, l)
            draw.text((10, 10),text,(0,0,0))

        r, g, b = realPicture.split()
        r = r.point(lambda i: i * 1.5)
        g = g.point(lambda i: i / 1.5)
        b = b.point(lambda i: i / 1.5)
        realPicture = Image.merge('RGB', (r,g,b))
        realPicture.save("terminated.png", "PNG")
        realPicture.show()

        return faces

    def faceFollow(self, motionObj, soundObj):
        print 'face follow'
        cams = self.visionProxy.getSubscribers()
        for cam in cams:
            self.visionProxy.unsubscribe(cam)
        haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        for n in range(0, 5):
            # try:
            print 'loop',n
            videoClient = self.visionProxy.subscribeCamera("python_client", 0, resolution, colorSpace, 5)
            self.visionProxy.setCameraParameter(videoClient, 18, 0)
            picture = self.visionProxy.getImageRemote(videoClient)
            self.visionProxy.unsubscribe(videoClient)
            picWidth = picture[0]
            picHeight = picture[1]
            array = picture[6]
            realPicture = Image.frombytes("RGB", (picWidth, picHeight), array)
            realPicture.save('image_{}.png'.format(n), "PNG")

            image = cv2.imread('image_{}.png'.format(n))
            faces = haar_face_cascade.detectMultiScale(image, minNeighbors=5); 
            print faces
            if len(faces)>0:
                soundObj.speak('face found')
                scale = 0
                (x, y, w, h) = faces[0]
                cx = x + w/2.
                cy = y + h/2.

                rotateX = -((cx/640.)-0.5)*60.97
                rotateY = ((cy/480.)-0.5)*np.radians(47.64)
                rotateX = rotateX//10*10
                motionObj.rotateTheta(rotateX)
                motionObj.moveHeadPitch(rotateY, 0.5)

                scale = np.sqrt(w**2 + h**2)
                dist = (-58./55.)*scale + 235.
                print 'distance:', dist
                if dist<50.:
                    break
                walksteps = max(((dist - 50)//8)*4, 8)

                print walksteps
                if walksteps>0:
                    motionObj.moveXYCm(walksteps,0)
            
            # except Exception, e:
            #     print e
                # self.visionProxy.unsubscribe(videoClient)
        print "done"
        soundObj.speak('Hi')
        motionObj.waveArm()

        pass
