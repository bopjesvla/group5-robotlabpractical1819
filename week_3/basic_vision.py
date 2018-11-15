'''
This is the basic tutorial, showing how to do some basic things with the Nao
* vision
'''
import naoqi
from naoqi import ALProxy
from PIL import Image
import vision_definitions


ip = '192.168.1.145'
port = 9559

resolution = vision_definitions.kVGA#kVGA #kQVGA  # QQVGA (160 * 120)
colorSpace = 11   # RGB

visionProxy = ALProxy("ALVideoDevice", ip, port)
motionProxy = ALProxy("ALMotion", ip, port)


def takePicture(theName):
    # motionObj.moveHeadPitch(0.3, 0.4)
    # time.sleep(2)
    videoClient = visionProxy.subscribeCamera("python_client", 0, resolution, colorSpace, 5)
    visionProxy.setCameraParameter(videoClient, 18, 0)
    picture = visionProxy.getImageRemote(videoClient)
    visionProxy.unsubscribe(videoClient)
    picWidth = picture[0]
    picHeight = picture[1]
    array = picture[6]
    realPicture = Image.frombytes("RGB", (picWidth, picHeight), array)
    realPicture.save(theName, "PNG")
    # realPicture.save("analyzeThis.png", "PNG")
    # Note: file name has to be written as 'filename.type' in order for the file to become 'type', even if you include the
    # parameter 'TYPE' after. If you do not, the file will be 'filename' without any type. It does seem the parameter "TYPE"
    # can be removed for png, but if it malfunctions, just use 'realPicture.save("filename.type", "TYPE").
    realPicture.show()

takePicture('analyzeTheName.png')
