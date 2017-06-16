#!/usr/bin/env python3
# -*- coding: <utf-8> -*-

#Author: Callum Pritchard, Joachim Hummel
#Project Name: Flick 3D Gesture
#Project Description: Sending Flick 3D Gesture sensor data to mqtt
#Version Number: 0.1
#Date: 15/6/17
#Release State: Alpha testing
#Changes: Created

#needed commands
# pip3 install paho-mqtt
# Run this line and Flick will be setup and installed
# curl -sSL https://pisupp.ly/flickcode | sudo bash

import signal
import flicklib
import time
import paho.mqtt.client as mqtt 
from curses import wrapper

some_value = 5000

def message(publisher, value):
    client = mqtt.Client()
    client.connect("mqtt.unixweb.de",1883,60)
    client.publish(publisher, value)
    client.disconnect()

@flicklib.move()
def move(x, y, z):
    global xyztxt
    xyztxt = '{:5.3f} {:5.3f} {:5.3f}'.format(x,y,z)

@flicklib.flick()
def flick(start,finish):
    global flicktxt
    flicktxt = 'FLICK-' + start[0].upper() + finish[0].upper()
    message('flick',flicktxt)

@flicklib.airwheel()
def spinny(delta):
    global some_value
    global airwheeltxt
    some_value += delta
    if some_value < 0:
        some_value = 0
    if some_value > 10000:
        some_value = 10000
    airwheeltxt = str(some_value/100)

@flicklib.double_tap()
def doubletap(position):
    global doubletaptxt
    doubletaptxt = position

@flicklib.tap()
def tap(position):
    global taptxt
    taptxt = position

@flicklib.touch()
def touch(position):
    global touchtxt
    touchtxt = position

def main():
    global xyztxt
    global flicktxt
    global airwheeltxt
    global touchtxt
    global taptxt
    global doubletaptxt

    xyztxt = ''
    flicktxt = ''
    flickcount = 0
    airwheeltxt = ''
    airwheelcount = 0
    touchtxt = ''
    touchcount = 0
    taptxt = ''
    tapcount = 0
    doubletaptxt = ''
    doubletapcount = 0

    while True:
        xyztxt = ''

        if len(flicktxt) > 0 and flickcount < 5:
            flickcount += 1
        else:
            flicktxt = ''
            flickcount = 0

        if len(airwheeltxt) > 0 and airwheelcount < 5:
            airwheelcount += 1
        else:
            airwheeltxt = ''
            airwheelcount = 0

        if len(touchtxt) > 0 and touchcount < 5:
            touchcount += 1
        else:
            touchtxt = ''
            touchcount = 0

        if len(taptxt) > 0 and tapcount < 5:
            tapcount += 1
        else:
            taptxt = ''
            tapcount = 0

        if len(doubletaptxt) > 0 and doubletapcount < 5:
            doubletapcount += 1
        else:
            doubletaptxt = ''
            doubletapcount = 0

        time.sleep(0.1)

main()
