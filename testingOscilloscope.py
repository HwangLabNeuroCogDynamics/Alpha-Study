from psychopy import visual, core

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,

                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
win = visual.Window([1680,1050],units='deg',fullscr=False,monitor='testMonitor')
import serial

port=serial.Serial('COM4',baudrate=115200) # based on the biosemi website-- may be wrong?

vis_deg=3.5
n_trials=100
no_stim=12

if no_stim==12:

    

    noon = visual.Circle(

        win=win, name='12',

        size=(0.60, 0.60),

        ori=0, pos=(0, vis_deg),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=0.0, interpolate=True)

    #noon.setAutoDraw(True)

    one_oclock = visual.Circle(

        win=win, name='1',

        size=(0.09, 0.15),

        ori=0, pos=((vis_deg/2), (sqrt(3)/2)*vis_deg),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-1.0, interpolate=True)

    #one_oclock.setAutoDraw(True)

    two_oclock = visual.Circle(

        win=win, name='2',

        size=(0.09, 0.15),

        ori=0, pos=(((sqrt(3)/2)*vis_deg), (vis_deg/2)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-2.0, interpolate=True)

    #two_oclock.setAutoDraw(True)

    three_oclock = visual.Circle(

        win=win, name='3',

        size=(0.09, 0.15),

        ori=0, pos=(vis_deg, 0),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-3.0, interpolate=True)

    #three_oclock.setAutoDraw(True)

    four_oclock = visual.Circle(

        win=win, name='4',

        size=(0.09, 0.15),

        ori=0, pos=(((sqrt(3)/2)*vis_deg), -(vis_deg/2)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-4.0, interpolate=True)

    #four_oclock.setAutoDraw(True)

    five_oclock = visual.Circle(

        win=win, name='5',

        size=(0.09, 0.15),

        ori=0, pos=((vis_deg/2), -((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-5.0, interpolate=True)

    #five_oclock.setAutoDraw(True)

    six_oclock = visual.Circle(

        win=win, name= '6', 

        size=(.09,0.15),  

        lineWidth=7, lineColor=None, fillColor=None,

        pos=(0, -vis_deg))

    #six_oclock.setAutoDraw(True)

    eleven_oclock = visual.Circle(

        win=win, name='11',

        size=(0.09, 0.15),

        ori=0, pos=((-vis_deg/2),(sqrt(3)/2)*vis_deg),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-1.0, interpolate=True)

    #eleven_oclock.setAutoDraw(True)

    ten_oclock = visual.Circle(

        win=win, name='10',

        size=(0.09, 0.15),

        ori=0, pos=(-((sqrt(3)/2)*vis_deg), (vis_deg/2)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-2.0, interpolate=True)

    #ten_oclock.setAutoDraw(True)

    nine_oclock = visual.Circle(

        win=win, name='9',

        size=(0.09, 0.15),

        ori=0, pos=(-vis_deg, 0),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-3.0, interpolate=True)

    #nine_oclock.setAutoDraw(True)

    eight_oclock = visual.Circle(

        win=win, name='8',

        size=(0.09, 0.15),

        ori=0, pos=(-((sqrt(3)/2)*vis_deg), -(vis_deg/2)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-4.0, interpolate=True)

    #eight_oclock.setAutoDraw(True)

    seven_oclock = visual.Circle(

        win=win, name='7',

        size=(0.09, 0.15),

        ori=0, pos=(-(vis_deg/2), -((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-5.0, interpolate=True)

    #seven_oclock.setAutoDraw(True)

    stimuli=[one_oclock,two_oclock,three_oclock,four_oclock,five_oclock,six_oclock,seven_oclock,eight_oclock,nine_oclock,ten_oclock,eleven_oclock,noon]

for stim in stimuli:
    stim.size=(1.5,1.5)
    stim.setLineColor([255,255,0],colorSpace='rgb255')
    stim.setFillColor(None)
    stim.autoDraw=True

redT=visual.ImageStim(win, image='C:\Stimuli\T2.png') 
redI=visual.ImageStim(win, image='C:\Stimuli\I3.png') #EEG stimulus presentation Dell
yellowT=visual.ImageStim(win, image='C:\Stimuli\YellowT.png')
redLpath='C:\Stimuli'
redL=[visual.ImageStim(win, image=redLpath+'\RedL copy 0.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 1.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 2.png'),
            visual.ImageStim(win, image=redLpath+'\RedL copy 3.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 4.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 5.png'),
            visual.ImageStim(win, image=redLpath+'\RedL copy 6.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 7.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 8.png')]

fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))
fixation.autoDraw=True
fixation.size=0.6
other_stim=sum([[redT],[redI],[yellowT],redL],[])

for a in range(len(other_stim)):
    let=other_stim[a]
    let.pos=stimuli[a].pos
    let.size=(1.25,1.25)
    let.autoDraw=True

for n in range(n_trials):
    port.close()
    
    fixation.draw()
    
    for stim in stimuli:
        stim.opacity=0
        stim.draw()
    for s in other_stim:
        s.opacity=0
        s.draw()
        
#    win.flip()
#    core.wait(.50844)

    for n in range(50):
        win.flip()
     
    for stim in stimuli:
        stim.opacity=1
        stim.draw()
    for s in other_stim:
        s.opacity=1
        s.draw()
    
    port.open()
    port.write(bytes([255]))
    #win.update()
    for n in range(50):
        win.flip()
    
    

#    win.flip()
#    core.wait(.50844)
    
