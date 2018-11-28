import multiprocessing
import Queue
import time
import signal
import sys
import naoqi
import numpy as np
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBroker

global IP
global PORT
PORT = 9559
IP = "192.168.1.103"

"""
In this tutorial I will show you how to make use Queues for concurrent programming in Python. Also demonstrates how to
have NAO judge how loud someone speaks.
You DO need a Nao for this part
"""


def writerone(queue):
    # Blue mood or red mood? Every ten seconds, we decide to change our mood, no matter what it is.
    name = multiprocessing.current_process().name
    print name, 'Starting'

    while True:
        queue.put(1)
        time.sleep(10)

    print name, 'Exiting'


def writertwo(queue):
    # Volume measure: this function will keep measuring the sound energy and put this in a queue. This function would at 0.5
    # for time.sleep be too fast for the reader: hence why it instead has to wait. This results in a bit of a slowdown to react
    # to sound, but at least the reader is no longer behind several seconds.
    name = multiprocessing.current_process().name
    print name, 'Starting'
    audioProxy = naoqi.ALProxy('ALAudioDevice', IP, PORT)
    audioProxy.enableEnergyComputation()
    while True:
        energy = audioProxy.getFrontMicEnergy()
        print energy
        queue.put(energy)
        time.sleep(1)
    audioProxy.disableEnergyComputation()
    print name, 'Exiting'


def readerone(queue1, queue2):
    # Adjusts the eyeleds of the robot: it colors them blue to red or otherwise every ten seconds depending on current color. If the sound energy
    # is higher than 1150 (this threshold varies per robot. Jarvis works with 1150.), show bright eyes; else show dimmed eyes.
    name = multiprocessing.current_process().name
    try:
        proxy = ALProxy("ALLeds", IP, PORT)
    except Exception as e:
        print "Could not create proxy to ALLeds"
        print "Error was: ", e
        sys.exit(1)
    time_out = 0.1
    print name, 'Starting'
    msg1 = []
    red = 0.0
    green = 0.0
    blue = 0.0
    duration = 0.5
    nameL = "FaceLeds"
    proxy.fadeRGB(nameL, red, green, blue, duration)
    msg2 = 0
    redEyes = False
    # Keep on doing this till thread is terminated.
    while True:
        # Figure out how loud the environment is.
        try:
            msg2 = queue2.get(True, time_out)
        # If the queue is empty, a Queue.Empty exception is thrown. This is likely to happen, so know how to handle it (for example, doing nothing).
        except Queue.Empty:
            pass
        if msg2 > 1150:
            strength = 1.0
        else:
            strength = 0.2
        # Figure out if we see blue ball and react to this.
        try:
            msg1 = queue1.get(True, time_out)
            # Switch redEyes.
            if redEyes:
                redEyes = False
            else:
                redEyes = True
        except Queue.Empty:
            pass
        if redEyes:
            blue = strength
            red = 0.0
        else:
            red = strength
            blue = 0.0
        proxy.fadeRGB(nameL, red, green, blue, duration)
    print name, 'Exiting'


if __name__ == '__main__':
    print 'starting'
    try:
        # Create processes and queues.
        q1 = multiprocessing.Queue()
        q2 = multiprocessing.Queue()
        writer1 = multiprocessing.Process(name='writer1-proc', target=writerone, args=(q1,))
        writer2 = multiprocessing.Process(name='writer2-proc', target=writertwo, args=(q2,))
        reader = multiprocessing.Process(name='reader-proc', target=readerone, args=(q1, q2,))
        # Start processes.
        writer1.start()
        writer2.start()
        reader.start()
        t = 1
        while t < 60:
            time.sleep(1)
            t += 1
            print t
        # End processes.
        print 'Ending program'
        # Forcibly end each thread.
        writer1.terminate()
        writer2.terminate()
        reader.terminate()
    except KeyboardInterrupt:
        print "Caught KeyboardInterrupt, terminating processes"
        writer1.terminate()
        writer2.terminate()
        reader.terminate()
