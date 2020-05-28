from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,

                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,

                   sqrt, std, deg2rad, rad2deg, linspace, asarray)

from numpy.random import random, randint, normal, shuffle,uniform
import os  # handy system and path functions
import sys  # to get file system encoding
import serial #for sending triggers from this computer to biosemi computer
import csv
from psychopy import visual, core
import pygame
from pygame import *
#import GLFW
import pyglet
from pyglet import *
from psychopy.hardware import joystick
#from psychopy.hardware import glfw

win = visual.Window([1680,1050],units='deg',winType='pyglet',fullscr=False,monitor='testMonitor',checkTiming=True)
joystick.backend='pyglet'
#joystick.backend='glfw'
joys=pyglet.input.get_joysticks()
if joys:
    print('joys')
    joys[0].open()
    
print
noButton=1
while noButton:
    print('no button')
    if joys[0].on_joybutton_press(joys[0],0):
        
        noButton=0
    
#pygame.init()
#joystick.init()
#xbox=pygame.joystick.Joystick(0)
#xbox.init()
#if (xbox.get_init() !=1) or (xbox.get_name()!='Controller (XBOX 360 For Windows)'):
#    print('ERRROROROROR')
#else:
#    print('all good')
#print(xbox.get_numballs())
#print(xbox.get_numbuttons())
#pygame.event.Event(7)
#pygame.event.clear()
#noButton=1
#while noButton:
#    for event in pygame.event.get():
#        print(event.type)
#        #print(xbox.get_ball())
#        if event.type==JOYBUTTONDOWN:
#            noButton=0


#xbobx1=joystick.XboxController(0)
#xbox1.get_a()