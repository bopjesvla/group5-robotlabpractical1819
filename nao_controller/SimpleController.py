'''
======================================================================================================
 https://github.com/redsphinx/Simple-NAO-Controller
 Written by Gabrielle Ras
 12 September 2014
 version 1.1

 This is a simple controller with an interface for the NAO that allows you to quickly take control of:
 - The limbs
 - The head
 - The camera
 - The speaker

 The required software version is naoqi 2.1
======================================================================================================
'''

import numpy as np
from Tkinter import *
from Config import Config
from SimpleMotions import SimpleMotions
from SimpleVisions import SimpleVisions
from SimpleSounds import SimpleSounds

from SimpleTouch import SimpleTouch

if Config.LINUX:
    sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % Config.LOCATION_NAOQI)

root = Tk()
root.wm_title("Simple NAO Controller v1.1")
root.configure(background="white")
frame = Frame(root, width=Config.FRAMEWIDTH, height=Config.FRAMEHEIGHT)
motionObj = SimpleMotions()
visionObj = SimpleVisions()
soundObj = SimpleSounds()

touchObj = SimpleTouch()

loopDelay = 100

class SimpleController:
    def __init__(self):
        frame.pack_propagate(0)
        self.createButtons()
        frame.pack()
        root.after(loopDelay, self.headTouch)
        root.mainloop()
        pass

    def headTouch(self):
        touchObj.task3(soundObj, motionObj)
        root.after(loopDelay, self.headTouch)

    def createButtons(self):
        standUpButton = Button( frame,
                text = "Stand Up",
                background = "green",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.fastStand()))
        standUpButton.pack()

        moveXYButton = Button(  frame,
                text = "Walk X/Y cm",
                background = "green",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.moveXYCm(self.moveX.get(), self.moveY.get())))

        moveXYButton.pack()

        def random_walk():
            self.wrapper(motionObj.moveXYCm(np.random.randint(-100, 40) * 4, 0))
            self.wrapper(motionObj.moveXYCm(0, np.random.randint(-100, 40) * 4))

        randButton = Button(  frame,
                text = "Random walk",
                background = "green",
                foreground = "black",
                command = random_walk)

        randButton.pack()


        armsButton = Button(  frame,
                text = "ARMS",
                background = "green",
                foreground = "black",
                command = lambda: self.wrapper(motionObj.arms()))

        armsButton.pack()

        self.makeXEntry()
        self.makeYEntry()

        rotateButton = Button(  frame,
                text = "Rotate in Degrees",
                background = "green",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.rotateTheta(self.moveTh.get())))
        rotateButton.pack()

        self.makeRotationThetaEntry()

        stopButton = Button(    frame,
                text = "STOP!",
                background = "red",
                foreground = "white",
                command = lambda : self.wrapper(motionObj.stop()))
        stopButton.pack()

        takePictureButton = Button( frame,
                text = "Take a Picture",
                background = "blue",
                foreground = "black",
                command = lambda : self.wrapper(visionObj.takePicture(self.name.get())))
        takePictureButton.pack()

        self.makePictureNameEntry()

        speakButton = Button(   frame,
                text = "Speak",
                background = "blue",
                foreground = "black",
                command = lambda : self.wrapper(soundObj.speak(self.message.get())))
        speakButton.pack()

        self.makeMessageEntry()

        moveHeadPitchButton = Button(   frame,
                text = "Move Head Pitch",
                background = "green",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.moveHeadPitch(self.headPitchTheta.get(), self.headPitchSpeed.get())))
        moveHeadPitchButton.pack()

        self.makeHeadPitchThetaEntry()
        self.makeHeadPitchSpeedEntry()

        chillOutButton = Button(    frame,
                text = "Chill Out",
                background = "pink",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.chillOut()))
        chillOutButton.pack()

        kickButton = Button(    frame,
                text = "Kick Right",
                background = "green",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.sideLeftKick()))
        kickButton.pack()

        
        restButton = Button(    frame,
                text = "Rest",
                background = "red",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.rest()))
        restButton.pack()

        btnSP = Button(   frame,
                text = "Shoulder Pitch",
                background = "blue",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.shoulderPitch( float(self.valSP.get()) )))
        btnSP.pack()
        self.valShoulderPitch()

        btnSR = Button(   frame,
                text = "Shoulder Roll",
                background = "blue",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.shoulderRoll( float(self.valSR.get()) )))
        btnSR.pack()
        self.valShoulderRoll()

        btnWave = Button(   frame,
                text = "Wave",
                background = "red",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.waveArm(  )))
        btnWave.pack()

        btnCome = Button(   frame,
                text = "Gesture Come",
                background = "red",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.gestureCome(  )))
        btnCome.pack()

    def makeXEntry(self):
        self.moveX = Entry(frame)
        self.moveX.pack()
        self.moveX.delete(0, END)
        self.moveX.insert(0, "enter in cm")
        pass

    def makeYEntry(self):
        self.moveY = Entry(frame)
        self.moveY.pack()
        self.moveY.delete(0, END)
        self.moveY.insert(0, "enter in cm")
        pass

    def makeRotationThetaEntry(self):
        self.moveTh = Entry(frame)
        self.moveTh.pack()
        self.moveTh.delete(0, END)
        self.moveTh.insert(0, "enter in degrees")
        pass

    def makePictureNameEntry(self):
        self.name = Entry(frame)
        self.name.pack()
        self.name.delete(0, END)
        self.name.insert(0, ".png")
        pass

    def makeMessageEntry(self):
        self.message = Entry(frame)
        self.message.pack()
        self.message.delete(0, END)
        self.message.insert(0, "Hello! I am a NAO")
        pass

    def valShoulderPitch(self):
        self.valSP = Entry(frame)
        self.valSP.pack()
        self.valSP.delete(0, END)
        self.valSP.insert(0, "1.0")
        pass

    def valShoulderRoll(self):
        self.valSR = Entry(frame)
        self.valSR.pack()
        self.valSR.delete(0, END)
        self.valSR.insert(0, "1.0")
        pass

    def wrapper(self, func):
        func
        root.update()
        #self.update()
        pass

    def makeHeadPitchThetaEntry(self):
        self.headPitchTheta = Entry(frame)
        self.headPitchTheta.pack()
        self.headPitchTheta.delete(0, END)
        self.headPitchTheta.insert(0, "0.3")
        pass

    def makeHeadPitchSpeedEntry(self):
        self.headPitchSpeed = Entry(frame)
        self.headPitchSpeed.pack()
        self.headPitchSpeed.delete(0, END)
        self.headPitchSpeed.insert(0, "0.5")
        pass

SimpleController = SimpleController()
