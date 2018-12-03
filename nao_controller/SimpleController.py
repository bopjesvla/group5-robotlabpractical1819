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

if Config.LINUX:
    sys.path.append('%s/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages' % Config.LOCATION_NAOQI)

root = Tk()
root.wm_title("Simple NAO Controller v1.1")
root.configure(background="white")
frame = Frame(root, width=Config.FRAMEWIDTH // 2, height=Config.FRAMEHEIGHT)
frame2 = Frame(root, width=Config.FRAMEWIDTH // 2, height=Config.FRAMEHEIGHT)

debug = True

if not debug:
    motionObj = SimpleMotions()
    visionObj = SimpleVisions()
    soundObj = SimpleSounds("SpeechRecognition")
    soundObj.getSpeech(['test', 'apple'], True)
    eyesObj = SimpleEyes()
    audioObj = SimpleAudio()
    touchObj = SimpleTouch()

loopDelay = 100

class SimpleController:
    def __init__(self):
        self.endIsNear = True
        frame.pack_propagate(0)
        self.createButtons()
        frame.pack(side='left')

        img = Image.open("terminated.png")
        tkimage = ImageTk.PhotoImage(img)
        self.panel = Label(frame2, image=tkimage)
        self.panel.pack()
        # self.panel.pack()

        frame2.pack(side='left')
        if not debug:
            root.after(loopDelay, self.passiveLoop)
        root.mainloop()
        pass

    def passiveLoop(self):
        # touchObj.task3(soundObj, motionObj)
        if(self.endIsNear):
            say = touchObj.oof()
            if say == 'reset':
                soundObj.speak('that went well')
                # motionObj.backToCenter()
            elif say:
                soundObj.speak(say)
            soundObj.checkSpeech()
        root.after(loopDelay, self.passiveLoop)

    def createButtons(self):
        standUpButton = Button( frame,
                text = "Stand Up",
                background = "green",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.fastStand()))
        standUpButton.pack()

        Button( frame,
                text = "sit",
                background = "green",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.sit())).pack()
        '''
        randButton = Button(  frame,
                text = "Random walk",
                background = "green",
                foreground = "black",
                              command = lambda : self.wrapper(motionObj.random_walk()))

        randButton.pack()

        moveXYButton = Button(  frame,
                text = "Walk X/Y cm",
                background = "green",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.moveXYCm(self.moveX.get(), self.moveY.get())))

        moveXYButton.pack()

        self.makeXEntry()
        self.makeYEntry()

        rotateButton = Button(  frame,
                text = "Rotate in Degrees",
                background = "green",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.rotateTheta(self.moveTh.get())))
        rotateButton.pack()

        self.makeRotationThetaEntry()
        '''

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
                command = lambda : self.wrapper(motionObj.moveHeadYaw(self.headPitchTheta.get(), self.headPitchSpeed.get())))
        moveHeadPitchButton.pack()

        self.makeHeadPitchThetaEntry()
        self.makeHeadPitchSpeedEntry()
        '''
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
        
        week2 = Label(frame, text="----- Week 2 -----")
        week2.pack()

        week2t1 = Label(frame, text="1. Random walk")
        week2t1.pack()

        btnWave = Button(   frame,
                text = "2. Wave",
                background = "red",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.waveArm(  )))
        btnWave.pack()

        btnCome = Button(   frame,
                text = "2. Gesture Come",
                background = "red",
                foreground = "black",
                command = lambda : self.wrapper(motionObj.gestureCome(  )))
        btnCome.pack()

        week2t1 = Label(frame, text="3. Touch Sit/Stand")
        week2t1.pack()

        week3 = Label(frame, text="----- Week 3 -----")
        week3.pack()

        week3t1 = Label(frame, text="1. Speech recognition")
        week3t1.pack()
        '''
        btnFaceFollow = Button(   frame,
                text = "2. Face Follow",
                background = "red",
                foreground = "black",
                command = lambda : self.wrapper( visionObj.faceFollow( motionObj , soundObj, self.panel, root )))
        btnFaceFollow.pack()

        def terminate():
            eyesObj.redEyes()
            loc = []

            while len(loc) < 1:
                loc = visionObj.terminator(self.panel, root, False)

            soundObj.speak("hasta la vista baby")
            eyesObj.blueEyes()

        terminatorButton = Button(    frame,
                text = "3. Terminate!",
                background = "green",
                foreground = "black",
                command = lambda : self.wrapper(terminate()))
        terminatorButton.pack()
        
        Button(    frame,
                text = "Rest",
                background = "red",
                foreground = "black",
                command = lambda : self.wrapper(self.rest2())).pack()

        '''
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
        '''

        Label(frame, text="----- Week 4 -----").pack()

        # week4t1 = Label(frame, text="1. Speech recognition")
        # week4t1.pack()

        # Button(   frame,
        #         text = "getAngles",
        #         background = "red",
        #         foreground = "black",
        #         # command = lambda : self.wrapper( audioObj.playThunder(  ))).pack()
        #         command = lambda : self.wrapper( motionObj.getAngles() )).pack()
        
        Button(   frame,
                text = "kneelPosture",
                background = "red",
                foreground = "black",
                # command = lambda : self.wrapper( audioObj.playThunder(  ))).pack()
                command = lambda : self.wrapper( motionObj.kneelPosture(  ))).pack()
          

        arrivalButton = Button(frame,
        text="Arrival",
        background="green",
        foreground="black",
        command=lambda: self.wrapper(arrival()))
        arrivalButton.pack()

        cutButton = Button(frame,
        text="Cut",
        background="green",
        foreground="black",
        command=lambda: self.wrapper(cut()))
        cutButton.pack()

        Button(frame,
        text="Clothing",
        background="blue",
        foreground="white",
        command=lambda: self.wrapper(clothing())).pack()

        # week 4 demo
        def arrival():
            motionObj.stand()
            motionObj.rotateTheta(140)
            #Step1: Eyes off
            eyesObj.noEyes()

            #Step2: Kneel
            motionObj.kneelPosture()

            #Step3: Thunder sound
            audioObj.playThunder() #Replace me with real code

            #Step4: Stand up from Kneeling
            motionObj.Crouch()
            motionObj.stand()

            #Step5: Level Head to horizontal
            motionObj.moveHeadPitch(-.3, 1)

            #Step6: White eyes when head is level
            eyesObj.whiteEyes()

            #Step7 & Step8: Terminator vision until 3 faces found
            faces = []

            #facePositions = [100./2., 100./2., 100.*-2., 100./-2., 100./-2.]
            facePositions = [-40, -20, 0, 20, 40]
            while len(faces) < 3:
                for p in facePositions:
                    faces = visionObj.terminator(self.panel, root)
                    if len(faces) > 2:
                        break
                    motionObj.moveHeadYaw(np.radians(p),0.1)
                    time.sleep(1)

            #Step9: Points to center face and speaks
            # faces.sort()
            (x, y, w, h) = faces[0]
            cx = x + w / 2.
            cy = y + h / 2.
            #Rotate head to look at center
            rotateX = -((cx / 640.) - 0.5) * 60.97
            rotateY = ((cy / 480.) - 0.5) * np.radians(47.64)
            rotateX = rotateX // 10 * 10
            motionObj.rotateTheta(rotateX)
            motionObj.moveHeadPitch(rotateY, 0.5)

            # motionObj.centerHead()
            print "head centering done"
            motionObj.point()
            soundObj.speak("Start process: Acquiring apparel")
            motionObj.handDown()

        def clothing_8():
			eyesObj.redEyes()
			soundObj.speak("I need your clothes, your boots and your motorcycle.")

        def clothing():
            print 'clothing'
            
            # return 0
            #==========================================

            print 'face follow'
            faces = visionObj.faceFollow(motionObj, soundObj, self.panel, root)
            print faces
            # TODO: do the calc to get turning angles from detected faces
            # return 0

            print 'target detection'
            facePositions = [-60, -40, -20, 0, 20, 40, 60]
            x = y = r = -1
            while x < 0:
                for p in facePositions:
                    result = visionObj.targetDetection()
                    if not result is None:
                        # TODO: "Not a match" on terminator vision
                        soundObj.speak("match")
                        x, y, r = result
                        print result
                        # TODO: center on the target
                        clothing_8()
                        while True:
                            say = touchObj.oof()
                            visionObj.terminator(self.panel, root, say is not None)
                        break
                    else:
                        # TODO: "Not a match" on terminator vision
                        soundObj.speak("not a match")
                        audioObj.playBoo()
                    motionObj.moveHeadYaw(np.radians(p),0.1)
            # soundObj.speak('clothing done')

        def cut():
            eyesObj.whiteEyes()
            soundObj.speak('that went well')
            motionObj.rotateTheta(140)
            motionObj.moveXYCm(120,0)
            motionObj.Crouch()

        ## week 5 demo
        Label(frame, text="----- Week 5 -----").pack()
        # start
        Button(frame,
            text="Start",
            background="blue",
            foreground="white",
            command=lambda: self.wrapper(w5Start())).pack()

        def w5Start():
            print 'w5 start'

        # come with me
        Button(frame,
            text="Come with me",
            background="blue",
            foreground="white",
            command=lambda: self.wrapper(w5ComeWithMe())).pack()

        def w5ComeWithMe():
            print 'w5ComeWithMe'

        # hasta la vista
        Button(frame,
            text="Hasta la Vista",
            background="blue",
            foreground="white",
            command=lambda: self.wrapper(w5HastaLaVista())).pack()

        def w5HastaLaVista():
            print 'w5HastaLaVista'


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

    def rest2(self):
        motionObj.sit()
        motionObj.stiffnessOff(motionObj.motionProxy)
        
    def wrapper(self, func):
        func
        # motionObj.sit()
        # motionObj.stiffnessOff(motionObj.motionProxy)
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

controller = SimpleController()
