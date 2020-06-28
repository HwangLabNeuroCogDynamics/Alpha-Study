from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,

                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,

                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle,uniform

win = visual.Window([1680,1050],units='deg',fullscr=False,monitor='testMonitor')
target_stim=visual.ImageStim(win, image='/Users/dcellier/Documents/GitHub/Alpha-Study/stimuli/T2.png') 
distractor_stim=visual.ImageStim(win, image='/Users/dcellier/Documents/GitHub/Alpha-Study/stimuli/I3.png')
vis_deg=3.5
no_stim=10
if no_stim==10:

    one_oclock = visual.Circle(

        win=win, name='1',

        size=(0.09, 0.15),

        ori=0, pos=((vis_deg/2), (sqrt(3)/2)*vis_deg),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-1.0, interpolate=True)

    one_oclock.setAutoDraw(True)

    two_oclock = visual.Circle(

        win=win, name='2',

        size=(0.09, 0.15),

        ori=0, pos=(((sqrt(3)/2)*vis_deg), (vis_deg/2)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-2.0, interpolate=True)

    two_oclock.setAutoDraw(True)

    three_oclock = visual.Circle(

        win=win, name='3',

        size=(0.09, 0.15),

        ori=0, pos=(vis_deg, 0),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-3.0, interpolate=True)

    three_oclock.setAutoDraw(True)

    four_oclock = visual.Circle(

        win=win, name='4',

        size=(0.09, 0.15),

        ori=0, pos=(((sqrt(3)/2)*vis_deg), -(vis_deg/2)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-4.0, interpolate=True)

    four_oclock.setAutoDraw(True)

    five_oclock = visual.Circle(

        win=win, name='5',

        size=(0.09, 0.15),

        ori=0, pos=((vis_deg/2), -((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-5.0, interpolate=True)

    five_oclock.setAutoDraw(True)

    eleven_oclock = visual.Circle(

        win=win, name='11',

        size=(0.09, 0.15),

        ori=0, pos=(-(vis_deg/2), ((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-1.0, interpolate=True)

    eleven_oclock.setAutoDraw(True)

    ten_oclock = visual.Circle(

        win=win, name='10',

        size=(0.09, 0.15),

        ori=0, pos=(-((sqrt(3)/2)*vis_deg), (vis_deg/2)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-2.0, interpolate=True)

    ten_oclock.setAutoDraw(True)

    nine_oclock = visual.Circle(

        win=win, name='9',

        size=(0.09, 0.15),

        ori=0, pos=(-vis_deg, 0),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-3.0, interpolate=True)

    nine_oclock.setAutoDraw(True)

    eight_oclock = visual.Circle(

        win=win, name='8',

        size=(0.09, 0.15),

        ori=0, pos=(-((sqrt(3)/2)*vis_deg), -(vis_deg/2)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-4.0, interpolate=True)

    eight_oclock.setAutoDraw(True)

    seven_oclock = visual.Circle(

        win=win, name='7',

        size=(0.09, 0.15),

        ori=0, pos=(-(vis_deg/2), -((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-5.0, interpolate=True)

    seven_oclock.setAutoDraw(True)

    stimuli=[one_oclock,two_oclock,three_oclock,four_oclock,five_oclock,seven_oclock,eight_oclock,nine_oclock,ten_oclock,eleven_oclock]
    right_stim=stimuli[:5]
    left_stim=stimuli[5:]

for stim in stimuli:

    stim.size=(1.5,1.5)
    stim.lineWidth=5
distractor_stim.size=([1.25,1.25])
target_stim.size=([1.25,1.25])

fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))

fixation.size=0.6
cue_types=['target','distractor']
order=np.random.choice((len(cue_types)+1),(len(cue_types)+1),replace=False) # num of conds in cue_types +1 for the neutral cue = 3  #this is randomly coming up with the indices of the conds in the scrambled list
cue_types_scramble=np.zeros(((len(cue_types)+1))) 
colors_scramble=np.zeros((3))
cues=['neutral']+cue_types #yields ['neutral','target','distractor'] so that the following for loop can select these and insert them into cue_types_scramble
colors=([-1,1,-1],[0,0,1],[1,1,0])
order=list(order)
cue_types_scramble=list(cue_types_scramble)
colors_scramble=list(colors_scramble)
for ind in order:
    cue_types_scramble[ind]=cues[order.index(ind)]
    colors_scramble[ind]=colors[order.index(ind)]
flex_cond_flag=True
def stim_preview(n_trials):
    intro_msg7= visual.TextStim(win, pos=[0, .5],units='norm', text='Now you will see a preview of the task.')
    intro_msg8= visual.TextStim(win, pos=[0, 0], units='norm',text='Please listen carefully to the experimenter while you watch the screen.')
    intro_msg9=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Please feel free to ask any clarifying questions after the fact.')
    intro_msg7.draw()
    intro_msg8.draw() 
    intro_msg9.draw()
    win.flip()
    core.wait(6)
    for demo_cue in cues:
        demo_msg= visual.TextStim(win, pos=[0, 0], units='norm',text=demo_cue+'cue demonstration')
        demo_msg.draw()
        win.update()
        core.wait(2.5)
        for n in range(n_trials):
            
            if not flex_cond_flag: 
                if n==0:
                    cue_target_1=np.random.choice(right_stim,1) 
                    cue_target_2=np.random.choice(left_stim,1)
            else: 
                cue_target_1=np.random.choice(right_stim,1)
                cue_target_2=np.random.choice(left_stim,1)
            cue_target_1[0].setLineColor(colors_scramble[cue_types_scramble.index(demo_cue)])
            cue_target_2[0].setLineColor(colors_scramble[cue_types_scramble.index(demo_cue)])
            win.flip()
            core.wait(.5)
        
            for circs in stimuli:
                print(circs)
                circs.setLineColor([0,0,0])
            win.flip()
            core.wait(1.5)
            
            target_loc1 = list(right_stim).index(cue_target_1[0]) 
            stim_minus_one = np.delete(right_stim, target_loc1) 
            target_loc2 = list(left_stim).index(cue_target_2[0]) 
            stim_minus_two = np.delete(left_stim,target_loc2) 
            which_circle= np.random.choice([cue_target_1[0], cue_target_2[0]],1)
            if which_circle[0]==cue_target_1[0]:
                other_circle=cue_target_2[0]
            else:
                other_circle=cue_target_1[0]
            if demo_cue=='target':
                target_stim.pos=which_circle[0].pos
                distractor_stim.pos=other_circle.pos
            elif demo_cue=='distractor':
                distractor_stim.pos=which_circle[0].pos
                target_stim.pos=other_circle.pos
            elif demo_cue=='neutral':
                which_circle=np.random.choice(stim_minus_one,1)
                other_circle=(np.random.choice(stim_minus_two,1))[0]
                target_stim.pos=(which_circle)[0].pos
                distractor_stim.pos=other_circle.pos
            which_circle[0].setLineColor=([1,-1,-1])
            other_circle.setLineColor=([1,-1,-1])
            target_stim.draw()
            distractor_stim.draw()
            win.flip()
            core.wait(1.5)

stim_preview(2)