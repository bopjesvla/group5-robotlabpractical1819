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
from PIL import Image, ImageTk, ImageOps
# import PIL?
import math
import numpy as np
from SimpleMotions import SimpleMotions
from Tkinter import Tk, Label

#global visionProxy
#resolution = 2    # VGA
resolution = vision_definitions.kVGA#kVGA #kQVGA  # QQVGA (160 * 120)
colorSpace = 11   # RGB
#colorSpace = vision_definitions. nt sure whats happening here
# motionObj = SimpleMotions()

class SimpleVisions:
    def __init__(self):
        self.visionProxy = ALProxy("ALVideoDevice", Config.ROBOT_IP, Config.PORT)
        self.motionProxy = ALProxy("ALMotion", Config.ROBOT_IP, Config.PORT)
        # rootImage = Tk()
        # img = Image.open("terminated.png")
        # tkimage = ImageTk.PhotoImage(img)
        # self.panel = Label(rootImage, image=tkimage)
        # self.panel.pack()
        # rootImage.mainloop()
        pass

    def showImage(self, img):
        img = Image.open("terminated.png")
        self.panel.configure(image=img)

    def terminator(self, distort=False, color="red"):
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
        for face in faces:
            (l, t, w, h) = face
            r = l + w
            b = t + h
            #realPicture.save("analyzeThis.png", "PNG")
            m[t:b,l-1:l+1,:] = 255
            m[t:b,r-1:r+1,:] = 255
            m[t-1:t+1,l:r,:] = 255
            m[b-1:b+1,l:r,:] = 255

        from PIL import ImageFont
        from PIL import ImageDraw

        if distort:
            m = self.distortion(m)

        realPicture = Image.fromarray(m)

        if len(faces) > 0:
            draw = ImageDraw.Draw(realPicture)
            # font = ImageFont.truetype(<font-file>, <font-size>)
            # draw.text((x, y),"Sample Text",(r,g,b))
            text = 't: {}\nb: {}\nr: {}\nl: {}'.format(t, b, r, l)
            draw.text((10, 10),text,(0,0,0))

        r, g, b = realPicture.split()

        #Week5 Hasta Step 3
        if (color == "green"):
            r = r.point(lambda i: i / 1.5)
            g = g.point(lambda i: i * 1.5)
            b = b.point(lambda i: i / 1.5)
        else:
            r = r.point(lambda i: i * 1.5)
            g = g.point(lambda i: i / 1.5)
            b = b.point(lambda i: i / 1.5)

        realPicture = Image.merge('RGB', (r,g,b))

        cv2.imshow('image',np.array(realPicture)[:, :, ::-1].copy())
        cv2.waitKey(10) & 0xFF

        # realPicture.save("terminated.png", "PNG")

        return faces

    def faceFollow(self, motionObj, soundObj, stopDist=100, wave=False):
        print 'face follow'
        cams = self.visionProxy.getSubscribers()
        for cam in cams:
            self.visionProxy.unsubscribe(cam)
        haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        dist_reached = False
        # facePositions = [0, 20, 40, 20, 0, -20, -40, -20, 0]

        for n in range(0, 5):
            print 'loop',n
            videoClient = self.visionProxy.subscribeCamera("python_client", 0, resolution, colorSpace, 5)
            self.visionProxy.setCameraParameter(videoClient, 18, 0)
            picture = self.visionProxy.getImageRemote(videoClient)
            self.visionProxy.unsubscribe(videoClient)
            picWidth = picture[0]
            picHeight = picture[1]
            array = picture[6]
            realPicture = Image.frombytes("RGB", (picWidth, picHeight), array)
            realPicture.save('facefollow_{}.png'.format(n), "PNG")

            # image = cv2.imread('image_{}.png'.format(n))
            image = np.array(realPicture)
            faces = haar_face_cascade.detectMultiScale(image, minNeighbors=5); 
            self.terminator()
            # print faces
            if len(faces)>0:
                if len(faces) > 3:
                    return_faces = faces
                # soundObj.speak('face found')
                scale = 0
                (x, y, w, h) = faces[0]
                cx = x + w/2.
                cy = y + h/2.

                rotateX = -((cx/640.)-0.5)*60.97
                rotateY = ((cy/480.)-0.5)*np.radians(47.64)
                rotateX = rotateX//10*10                
                if rotateX!=0.0:
                    print rotateX
                    motionObj.rotateTheta(rotateX)
                    motionObj.moveHeadPitch(rotateY, 0.5)

                scale = np.sqrt(w**2 + h**2)
                dist = (-58./55.)*scale + 235.
                print 'distance:', dist
                if dist<stopDist:
                    dist_reached = True
                    break
                # walksteps = max(((dist - stopDist)//8)*4, 8) # 50%
                walksteps = max(((dist - stopDist)*3//16)*4, 8) #75%
                
                print walksteps
                if walksteps>0:
                    motionObj.moveXYCm(walksteps,0)

        if wave:
            soundObj.speak('Hi')
            motionObj.waveArm()
        if dist_reached:
            print "target reached"
            motionObj.stand()
        print "Face follow done"
        pass
    
    def targetDetection(self):
        cams = self.visionProxy.getSubscribers()
        for cam in cams:
            self.visionProxy.unsubscribe(cam)

        # for n in range(0, 5):
        n=0
        video = True
        balldetect = True
        print 'loop',n
        realPicture = None
        if(video):
            videoClient = self.visionProxy.subscribeCamera("python_client", 0, resolution, colorSpace, 5)
            self.visionProxy.setCameraParameter(videoClient, 18, 0)
            picture = self.visionProxy.getImageRemote(videoClient)
            self.visionProxy.unsubscribe(videoClient)
            picWidth = picture[0]
            picHeight = picture[1]
            array = picture[6]
            realPicture = Image.frombytes("RGB", (picWidth, picHeight), array)
            realPicture.save('save_{}.png'.format(n), "PNG")
            # realPicture.show()

        
        if(balldetect):
            image = np.array(realPicture)
            # image = cv2.imread("save_3.png")

            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # image = Image.fromarray(image)
            # image.show()

            lower_green = np.array([36,100,100], dtype = np.uint8)
            upper_green = np.array([86,255,255], dtype=np.uint8)

            #convert to a hsv colorspace
            hsvImage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

            #Create a treshold mask
            color_mask=cv2.inRange(hsvImage,lower_green,upper_green)

            #apply the mask on the image
            green_image = cv2.bitwise_and(image,image,mask=color_mask)

            kernel=np.ones((9,9),np.uint8)
            #Remove small objects
            opening =cv2.morphologyEx(color_mask,cv2.MORPH_OPEN,kernel)
            #Close small openings
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
            #Apply a blur to smooth the edges
            smoothed_mask = cv2.GaussianBlur(closing, (9,9),0)

            #Apply our (smoothend and denoised) mask
            #to our original image to get everything that is blue.
            green_image = cv2.bitwise_and(image,image,mask=smoothed_mask)

            #Get the grayscale image (last channel of the HSV image
            gray_image = green_image[:,:,2]

            #Use a hough transform to find circular objects in the image.
            circles = cv2.HoughCircles(
                gray_image,             #Input image to perform the transformation on
                cv2.HOUGH_GRADIENT,     #Method of detection
                1,                      #Ignore this one
                50,                      #Min pixel dist between centers of detected circles
                param1=200,             #Ignore this one as well
                param2=20,              #Accumulator threshold: smaller = the more (false) circles
                minRadius=5,            #Minimum circle radius
                maxRadius=100)          #Maximum circle radius
            
            if circles is not None:
                # print(circles)
                # for x, y, r in circles[0]:
                #     cv2.circle(image, (x, y), r, (255, 255, 0), 5)
                return circles[0][0]
            # imagePil = Image.fromarray(image)
            # imagePil.save('balldect_{}.png'.format(n), "PNG")
            # imagePil.show()


    def distortion(self, img):
        # Distortion filter on camera
        picWidth = img.shape[0]
        picHeight = img.shape[1]

        imageArr = img
        A= picWidth / 3.0
        W = 2.0/picHeight

        shift = lambda x: A * np.sin(2.0*np.pi*x*W)
        for i in range (picWidth):
            imageArr[:,i] = np.roll(img[:,i], int (shift(i)))

        return imageArr
