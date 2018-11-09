'''
This is the basic tutorial, showing how to do some basic things with the Nao
* motion
'''

# from naoqi_hacky import naoqi
import naoqi
# from naoqi_hacky import almath
import random
import motion

# --------------------------------------------------------------------------------------
# Initialize proxies
# --------------------------------------------------------------------------------------
ip = '192.168.1.103'
port = 9559
motionProxy = naoqi.ALProxy('ALMotion', ip, port)
postureProxy = naoqi.ALProxy('ALRobotPosture', ip, port)

# --------------------------------------------------------------------------------------
# Movement: Postures

# goToPosture is 'smart' i.e. it will go to this posture from any position. It tries
# to avoid collision with itself and tries to maintain balance. Might take multiple steps
# Opposite: applyPosture, it's a blocking call (can be made none blocking with post? Look into this)
# --------------------------------------------------------------------------------------
def do_postures():
    # pass name of posture as string and speed as float between 0.0 and 1.0
    print 'standing up'
    postureProxy.goToPosture('Stand', 0.8)
    print 'standing'
    postureProxy.goToPosture('Sit', 0.8)

    # prints all available postures
    print postureProxy.getPostureList()


# --------------------------------------------------------------------------------------
# Motion: basic walking in some direction

# x: positive move forward, negative move backwards [-1.0 to 1.0]
# y: positive left, negative right [-1.0 to 1.0]
# theta: positive for counterclockwise, negative for clockwise [-1.0 to 1.0]
# speed: determines the frequency of the steps, so the velocity [0.0 to 1.0]
# --------------------------------------------------------------------------------------
def walk(x, y, theta, speed):
    motionProxy.wakeUp()
    postureProxy.goToPosture('Stand', 0.5)
    x = float(x)
    y = float(y)
    theta = float(theta)
    speed = float(speed)
    motionProxy.setWalkTargetVelocity(x, y, theta, speed)
    relax()

# --------------------------------------------------------------------------------------
# Motion: shutting down the motors, "relaxes the Nao muscles"
# --------------------------------------------------------------------------------------
def relax():
    postureProxy.goToPosture('Sit', 0.5)
    motionProxy.rest()  # Shuts down motors

# --------------------------------------------------------------------------------------
# Movement: Move head

# Yaw and pitch angles are in radians.
# Pitch is float between 0.0 and 1.0
# --------------------------------------------------------------------------------------
def move_head_to(yaw, pitch, speed=0.10):
    motionProxy.rest()
    # Names of the joints
    joints = ['HeadYaw', "HeadPitch"]
    motionProxy.setStiffnesses(joints, 0.8)
    # list of the angles (in radians)
    angles = [yaw, pitch]
    # You need to pass a list of names, list of angles and the speed of execution.
    motionProxy.setAngles(joints, angles, speed)
    # Some examples:
    # motionProxy.setAngles(joints, [-1, 0.5], speed)
    # motionProxy.setAngles(joints, [-1, -0.5], speed)
    # motionProxy.setAngles(joints, [1, -0.5], speed)

# --------------------------------------------------------------------------------------
# Motion: Checking if position is valid
# --------------------------------------------------------------------------------------
def is_valid_pos(x, y, z):
    x_lim = (0, 0.2)
    y_lim = (-0.3, 0.3)
    z_lim = (0.0, 0.3)

    if x_lim[0] <= x <= x_lim[1]:
        if y_lim[0] <= y <= y_lim[1]:
            if z_lim[0] <= z <= z_lim[1]:
                return True
            else:
                print('z out of range %s' % str(z_lim))
                return False
        else:
            print('y out of range %s' % str(y_lim))
            return False
    else:
        print('x out of range %s' % str(x_lim))
        return False


# --------------------------------------------------------------------------------------
# Motion: Cartesian movement example with right arm
# --------------------------------------------------------------------------------------
def cartesian_rarm_movement(x, y, z):
    if is_valid_pos(x, y, z):
        effector = 'RArm'
        frame = motion.FRAME_TORSO
        axisMask = almath.AXIS_MASK_VEL
        targetPos = almath.Position3D(x, y, z)
        print targetPos
        targetTf = almath.transformFromPosition3D(targetPos)
        path = []
        path.append(list(targetTf.toVector()))

        times = [5.0]
        motionProxy.transformInterpolations(effector, frame, path, axisMask, times)

        return True

    else:
        return False


# --------------------------------------------------------------------------------------
# Motion: make a random valid movement with the right arm
# --------------------------------------------------------------------------------------
def random_cartesian_rarm_movement():
    # open the right hand
    motionProxy.openHand('RHand')
   
    effector = "RArm"
    frame = motion.FRAME_TORSO
    axisMask = almath.AXIS_MASK_VEL

    # random positions
    x = random.uniform(0, 0.2)
    y = random.uniform(-.3, .3)
    z = random.uniform(.0, .3)

    if is_valid_pos(x, y, z):
        targetPos = almath.Position3D(x, y, z)
        print targetPos
        targetTf = almath.transformFromPosition3D(targetPos)
        path = list(targetTf.toVector())

        # Go to the target and back again
        times = [5.0]  # seconds
        motionProxy.setStiffnesses(effector, 0.6)
        motionProxy.transformInterpolations(effector, frame, path, axisMask, times)


# --------------------------------------------------------------------------------------
# Motion: blocking movement example with the head joints
# --------------------------------------------------------------------------------------
def blocking_head_movement():
    postureProxy.goToPosture('Sit', 1.0)
    motionProxy.rest()

    joints = 'HeadYaw'
    angles = 1.0
    times = 1.0  # time in seconds
    isAbsolute = True
    motionProxy.setStiffnesses('Head', 0.8)
    motionProxy.angleInterpolation(joints, angles, times, isAbsolute)

    angles = [0, 1, 0]
    times = [1, 2, 2.5]
    motionProxy.angleInterpolation(joints, angles, times, isAbsolute)

    joints = ['HeadYaw', 'HeadPitch']
    angles = [1, -0.5]
    times = [1, 1.5]
    motionProxy.angleInterpolation(joints, angles, times, isAbsolute)
