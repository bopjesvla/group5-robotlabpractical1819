'''
http://doc.aldebaran.com/2-1/naoqi/audio/alspeechrecognition-api.html
This is the basic tutorial, showing how to do some basic things with the Nao
* audio
'''

import time
from naoqi import ALProxy


ip = '192.168.1.102'
port = 9559

# Creates a proxy on the speech-recognition module
speechProxy = ALProxy("ALSpeechRecognition", ip, port)

speechProxy.setLanguage("English")

# Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
vocabulary = ['cookie', 'robot', 'yumyum']
speechProxy.setVocabulary(vocabulary, False)

# Start the speech recognition engine with user Test_speechProxy
speechProxy.subscribe("Test_ASR")
print 'Speech recognition engine started'
time.sleep(20)
speechProxy.unsubscribe("Test_ASR")