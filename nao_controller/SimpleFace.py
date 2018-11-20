import time

from naoqi import ALProxy
from Config import Config

# Create a proxy to ALFaceDetection
try:
    faceProxy = ALProxy("ALFaceDetection", Config.ROBOT_IP, Config.PORT)
except Exception, e:
    print "Error when creating face detection proxy:"
    print str(e)
    exit(1)

# Subscribe to the ALFaceDetection proxy
# This means that the module will write in ALMemory with
# the given period below
period = 500
faceProxy.subscribe("Test_Face", period, 0.0 )

# ALMemory variable where the ALFacedetection modules
# outputs its results
memValue = "FaceDetected"

# Create a proxy to ALMemory
try:
    memoryProxy = ALProxy("ALMemory", Config.ROBOT_IP, Config.PORT)
except Exception, e:
    print "Error when creating memory proxy:"
    print str(e)
    exit(1)

def get_face():
    val = memoryProxy.getData(memValue)

    print ""
    print "*****"
    print ""

    # Check whether we got a valid output.
    if(val and isinstance(val, list) and len(val) >= 2):

        # We detected faces !
        # For each face, we can read its shape info and ID.

        # First Field = TimeStamp.
        timeStamp = val[0]

        # Second Field = array of face_Info's.
        faceInfoArray = val[1]

        try:
            # Browse the faceInfoArray to get info on each detected face.
            for j in range( len(faceInfoArray)-1 ):
                faceInfo = faceInfoArray[j]

            # First Field = Shape info.
            faceShapeInfo = faceInfo[0]

            # Second Field = Extra info (empty for now).
            faceExtraInfo = faceInfo[1]

            return faceShapeInfo

        except Exception, e:
            print "faces detected, but it seems getData is invalid. ALValue ="
            print val
            print "Error msg %s" % (str(e))
    else:
        return None

# A simple loop that reads the memValue and checks whether faces are detected.
if __name__ == "__main__":
    for i in range(0, 20):
        time.sleep(0.5)
        get_face()
    faceProxy.unsubscribe("Test_Face")
    print "Test terminated successfully."

# Unsubscribe the module.

