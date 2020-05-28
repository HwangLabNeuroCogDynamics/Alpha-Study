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


win = visual.Window([1680,1050],units='deg',fullscr=False,monitor='testMonitor',checkTiming=True)
A = visual.TextStim(win, text='A',units='norm', color=(1,1,1))
B = visual.TextStim(win, text='B',units='norm', color=(1,1,1))

A.draw()
core.wait(2)
win.flip()
event.waitKeys(keyList='^')
win.flip()
B.draw()
win.flip()
core.wait(2)