'''
======================================================================================================
 https://github.com/redsphinx/Simple-NAO-Controller
 Written by Gabrielle Ras
 12 September 2014 
 version 1.1

 This is a py file containing global final variables.

 The required software version is naoqi 2.1
======================================================================================================
'''
import math
from sys import platform
import os
#import almath

class Config:

    LINUX = platform == 'linux' or platform == 'linux2'

    if LINUX:
        print('-- User has Linux system according to the Config.py')
        LOCATION_NAOQI = open('../LOCATION').read().strip()
        if LOCATION_NAOQI == '/home/user/location/to/be/set':
            print('-- Error: please specify the NAOqi location')
        print('-- NAOqi location set to %s' % LOCATION_NAOQI)
    else:
        LOCATION_NAOQI = None

    # if os.getlogin() == 'bob':
    #     ROBOT_IP = 'localhost'
    # else:
    #     ROBOT_IP = '192.168.1.104'

    # Connection
    ROBOT_IP = '192.168.1.144'
    PORT = 9559

    print('-- Config robot IP: %s' % ROBOT_IP)


    # Conversions
    DEG2RAD = math.pi/180.0 # Convert Deg to Rad
    RAD2DEG = 180.0/math.pi # Convert Rad to Deg

    # Interface things
    FRAMEWIDTH = 300
    FRAMEHEIGHT = 800

    # Movement
    MAXSTEPSIZE = 8  # cm
    MINSTEPSIZE = 4  # cm
    MAXTHETA = 30  # in degrees CHANGED TO RADIANS IN CALCULATIONS
    MINTHETA = 10  #  in degrees CHANGED TO RADIANS IN CALCULATIONS
    UNIT = 4  # cm, the unit of distance in our case. so the robot moves in multiplicities of this unit
    THETAUNIT = 10
    RLEG = "RLeg"
    LLEG = "LLeg"
    SPEED = 1.0  # decrease to increase accuracy, robot will move slower though
    DIRECTIONS = ["L", "R", "Fw", "Bw"]


    # Vision
    CAMERA_H_FOV = 46.4 * DEG2RAD # Horizontal field of view
    CAMERA_V_FOV = 34.8 * DEG2RAD # Vertical field of view
    RESW = 320#640#320 #160.0 #Capture width
    RESH = 240#480#240 #120.0 #Capture height
    FOVHOR = 46.40 #"horizontal" field of view
    FOVVER = 34.80 #"vertical" field of view
