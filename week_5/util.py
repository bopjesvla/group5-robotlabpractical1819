"""
Functions to use with nao_example.py
"""
import time


def init_leds(proxy):
    red_leds = [
        'Face/Led/Red/Left/0Deg/Actuator/Value',
        'Face/Led/Red/Left/45Deg/Actuator/Value',
        'Face/Led/Red/Left/90Deg/Actuator/Value',
        'Face/Led/Red/Left/135Deg/Actuator/Value',
        'Face/Led/Red/Left/180Deg/Actuator/Value',
        'Face/Led/Red/Left/225Deg/Actuator/Value',
        'Face/Led/Red/Left/270Deg/Actuator/Value',
        'Face/Led/Red/Left/315Deg/Actuator/Value',
        'Face/Led/Red/Right/0Deg/Actuator/Value',
        'Face/Led/Red/Right/45Deg/Actuator/Value',
        'Face/Led/Red/Right/90Deg/Actuator/Value',
        'Face/Led/Red/Right/135Deg/Actuator/Value',
        'Face/Led/Red/Right/180Deg/Actuator/Value',
        'Face/Led/Red/Right/225Deg/Actuator/Value',
        'Face/Led/Red/Right/270Deg/Actuator/Value',
        'Face/Led/Red/Right/315Deg/Actuator/Value'
    ]
    green_leds = [
        'Face/Led/Green/Left/0Deg/Actuator/Value',
        'Face/Led/Green/Left/45Deg/Actuator/Value',
        'Face/Led/Green/Left/90Deg/Actuator/Value',
        'Face/Led/Green/Left/135Deg/Actuator/Value',
        'Face/Led/Green/Left/180Deg/Actuator/Value',
        'Face/Led/Green/Left/225Deg/Actuator/Value',
        'Face/Led/Green/Left/270Deg/Actuator/Value',
        'Face/Led/Green/Left/315Deg/Actuator/Value',
        'Face/Led/Green/Right/0Deg/Actuator/Value',
        'Face/Led/Green/Right/45Deg/Actuator/Value',
        'Face/Led/Green/Right/90Deg/Actuator/Value',
        'Face/Led/Green/Right/135Deg/Actuator/Value',
        'Face/Led/Green/Right/180Deg/Actuator/Value',
        'Face/Led/Green/Right/225Deg/Actuator/Value',
        'Face/Led/Green/Right/270Deg/Actuator/Value',
        'Face/Led/Green/Right/315Deg/Actuator/Value'
    ]
    blue_leds = [
        'Face/Led/Blue/Left/0Deg/Actuator/Value',
        'Face/Led/Blue/Left/45Deg/Actuator/Value',
        'Face/Led/Blue/Left/90Deg/Actuator/Value',
        'Face/Led/Blue/Left/135Deg/Actuator/Value',
        'Face/Led/Blue/Left/180Deg/Actuator/Value',
        'Face/Led/Blue/Left/225Deg/Actuator/Value',
        'Face/Led/Blue/Left/270Deg/Actuator/Value',
        'Face/Led/Blue/Left/315Deg/Actuator/Value',
        'Face/Led/Blue/Right/0Deg/Actuator/Value',
        'Face/Led/Blue/Right/45Deg/Actuator/Value',
        'Face/Led/Blue/Right/90Deg/Actuator/Value',
        'Face/Led/Blue/Right/135Deg/Actuator/Value',
        'Face/Led/Blue/Right/180Deg/Actuator/Value',
        'Face/Led/Blue/Right/225Deg/Actuator/Value',
        'Face/Led/Blue/Right/270Deg/Actuator/Value',
        'Face/Led/Blue/Right/315Deg/Actuator/Value',
    ]

    proxy.createGroup('red_leds', red_leds)
    proxy.createGroup('green_leds', green_leds)
    proxy.createGroup('blue_leds', blue_leds)


def eyes_turn(proxy, color):
    list_colors = ['red', 'green', 'blue']
    assert (color in list_colors)

    # turn off all leds
    [proxy.off('%s_leds' % clr) for clr in list_colors]

    # turn on only the desired color
    proxy.on('%s_leds' % color)


def eyes_rgb(proxy):
    list_colors = ['red', 'green', 'blue']
    cycle = 6

    for c in range(cycle):
        for clr in list_colors:
            eyes_turn(proxy, clr)
            time.sleep(0.5)
