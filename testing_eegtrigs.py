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

expInfo = {'subject': '', 'session': '01'}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expName='alpha_pilot'
win = visual.Window([1680,1050],units='deg',fullscr=False,monitor='testMonitor')
no_stim=6
vis_deg=3.5

redT=visual.ImageStim(win, image='C:\Stimuli\T2.png') 
redI=visual.ImageStim(win, image='C:\Stimuli\I3.png') #EEG stimulus presentation Dell
yellowT=visual.ImageStim(win, image='C:\Stimuli\YellowT.png')
redLpath='C:\Stimuli'
filename='Z:/AlphaStudy_Data/eegData'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])
refresh_rate=50
redL=[visual.ImageStim(win, image=redLpath+'\RedL copy 0.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 1.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 2.png'),
    visual.ImageStim(win, image=redLpath+'\RedL copy 3.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 4.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 5.png'),
    visual.ImageStim(win, image=redLpath+'\RedL copy 6.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 7.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 8.png')]
distractor_stim=yellowT
target_stim=redT
other_stim=redL

other=0.95
chance=(1/6)*2
cue_types=['target','distractor']
cue_valid=[other,chance]
stimList=[]
for cue in cue_types:
    for num in cue_valid:
        stimList.append({'cue':cue,'validity':num})

num_trials=3
num_reps=1

def make_ITI(exp_type):
    if exp_type=='b' or exp_type=='m' or exp_type=='d':
        ITI=np.random.choice([1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6],1)[0] #averages to around 2 second?
    elif exp_type=='e':
        ITI=np.random.choice([3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6],1)[0] # averages to around 4 seconds?
    return ITI

if no_stim==6:
    one_oclock = visual.Circle(
    
            win=win, name='1',
    
            size=(0.09, 0.15),
    
            ori=0, pos=((vis_deg/2), (sqrt(3)/2)*vis_deg),
    
            lineWidth=7, lineColor=None, lineColorSpace='rgb',
    
            fillColor=None, fillColorSpace='rgb',
    
            opacity=1, depth=-1.0, interpolate=True)
    
    one_oclock.setAutoDraw(True)
    three_oclock = visual.Circle(
        win=win, name='3',

        size=(0.09, 0.15),

        ori=0, pos=(vis_deg, 0),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-3.0, interpolate=True)

    three_oclock.setAutoDraw(True)
    
    five_oclock = visual.Circle(

        win=win, name='5',

        size=(0.09, 0.15),

        ori=0, pos=((vis_deg/2), -((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-5.0, interpolate=True)

    five_oclock.setAutoDraw(True)
    seven_oclock = visual.Circle(

        win=win, name='7',

        size=(0.09, 0.15),

        ori=0, pos=(-(vis_deg/2), -((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-5.0, interpolate=True)

    seven_oclock.setAutoDraw(True)
    nine_oclock = visual.Circle(

        win=win, name='9',

        size=(0.09, 0.15),

        ori=0, pos=(-vis_deg, 0),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-3.0, interpolate=True)

    nine_oclock.setAutoDraw(True)
    eleven_oclock = visual.Circle(

        win=win, name='11',

        size=(0.09, 0.15),

        ori=0, pos=(-(vis_deg/2), ((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-1.0, interpolate=True)

    eleven_oclock.setAutoDraw(True)
    stimuli=[one_oclock,three_oclock,five_oclock,seven_oclock,nine_oclock,eleven_oclock]
    right_stim=stimuli[:3]
    left_stim=stimuli[3:]

for stim in stimuli:
    stim.size=(1.5,1.5)
    stim.lineWidth=5
distractor_stim.size=([1.25,1.25])
target_stim.size=([1.25,1.25])
for stim in other_stim:
    stim.size=([1.25,1.25])
fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))
fixation.size=0.6

EEGflag=1
if EEGflag: 
    startSaveflag=bytes([254])
    port=serial.Serial('COM4',baudrate=115200)

order=np.random.choice(len(cue_types),len(cue_types),replace=False) # num of conds in cue_types #this is randomly coming up with the indices of the conds in the scrambled list
cue_types_scramble=np.zeros((len(cue_types))) 
colors_scramble=np.zeros((2))
cues=cue_types #yields ['target','distractor'] so that the following for loop can select these and insert them into cue_types_scramble
colors=([-1,-1,1],[-1,1,-1]) 
order=list(order)
cue_types_scramble=list(cue_types_scramble)
colors_scramble=list(colors_scramble)
for ind in order:
    cue_types_scramble[ind]=cues[order.index(ind)]
    colors_scramble[ind]=colors[order.index(ind)]

cue_VnL=[] #here, we're initiating a list of the validities and the lateralizations (bilateral or unilateral) and pairing them for however many times they need to be carried out (2)

for c in cue_valid:
    for lattype in ['bi','uni']:
        for n in range(num_reps):
            cue_VnL.append([c,lattype])

order2=np.random.choice(len(cue_VnL),len(cue_VnL),replace=False) #this is going to be the order that we ultimately call ea of the conditions in
order2=list(order2)
cue_VnL_scramble=np.zeros((len(cue_VnL)))
cue_VnL_scramble=list(cue_VnL_scramble)
for ind2 in order2:
    cue_VnL_scramble[ind2]=cue_VnL[order2.index(ind2)]

print(cue_types_scramble)
print(cue_VnL_scramble)

k=0
for cue in cue_types_scramble: #looping through the types of cues in sequence, since we care about the order now. 
    
    reps=len(cue_VnL_scramble)
    
    for block in (range(reps)): #we want each cue type to repeat (num_reps * the # of validity conds * 2 laterality conds) times 
        
        blockLat=cue_VnL_scramble[block][1]
        thisValid=cue_VnL_scramble[block][0]
        trialDataList=[]
        thisBlock=stimList[stimList.index({'cue':cue,'validity':thisValid})]
        
        for n in range(num_trials):
            ITI=make_ITI('e')
            
            if n==0:
                for circs in stimuli:
                    circs.opacity = 0 
                info_msg=visual.TextStim(win, pos=[0,.5],units='norm',text='This block will show %s cues' %thisBlock['cue']) 
                info_msg.draw()
                info_msg2=visual.TextStim(win, pos=[0,-.5], units='norm',text='Press any key to continue')
                info_msg2.draw()
                win.update()
                key1=event.waitKeys()
                fixation.draw()
                win.flip() 
                core.wait(3)# pre-block pause
            
            for circs in stimuli:
                circs.opacity=1
                circs.setLineColor([0,0,0])
                circs.setFillColor([0,0,0])
             
            if blockLat=='uni':
                cue_target_1=np.random.choice(stimuli,1)
            else:
                cue_target_1=np.random.choice(right_stim,1)
                cue_target_2=np.random.choice(left_stim,1)
            
            color_ind=cue_types_scramble.index(thisBlock['cue'])
            cue_target_1[0].setLineColor(colors_scramble[color_ind])
            if not (blockLat=='uni'):
                cue_target_2[0].setLineColor(colors_scramble[color_ind])
            
            if EEGflag:
                port.close()
                port.open()
                port.write(startSaveflag)
                port.flush()
                core.wait(.2)
                port.close()
            
            win.flip()
            core.wait(.5)
            
            fixation.draw()
            for circs in stimuli:
                circs.setLineColor([0,0,0])
            
            win.flip()
            core.wait(1.5)
            
            fixation.draw()
            odds=thisBlock['validity']
            
            if not (blockLat=='uni'):
                target_loc1 = list(right_stim).index(cue_target_1[0]) #where are the two cued circles?
                stim_minus_one = np.delete(right_stim, target_loc1)
                target_loc2 = list(left_stim).index(cue_target_2[0]) 
                stim_minus_two = np.delete(left_stim,target_loc2) #get a list of stimuli that don't include cued circles
                stim_minus_both=list(stim_minus_one)+list(stim_minus_two)
                which_circle= np.random.choice([cue_target_1[0], cue_target_2[0], stim_minus_both],1,p=[(odds/2),(odds/2),(1-odds)]) #decide if cue is valid, using validity % of this condition
            elif blockLat=='uni':
                target_loc=stimuli.index(cue_target_1[0]) #may error
                stim_minus_one=np.delete(stimuli, target_loc)
                if odds==chance:
                    p=[(odds/2),(1-(odds/2))] #because the 'chance' validity is calculated assuming that there are 2 cued circles, we have to divide it by 2
                else:
                    p=[odds,(1-odds)]
                which_circle=np.random.choice([cue_target_1[0],stim_minus_one],1,p=p)
            
            if not (blockLat=='uni'): #if we have bilateral cues
                if (which_circle[0] in cue_target_1):
                    trial_type='valid'
                    cue_side='R'
                elif (which_circle[0] in cue_target_2): #if the dis or target is in one of the circles cued, it was a predictive trial. SAVE OUT this info later!!!!!
                    trial_type='valid'
                    cue_side='L'
                else:
                    trial_type='invalid'
            elif blockLat=='uni': #if we have unilateral cue
                if which_circle[0] in cue_target_1:
                    trial_type='valid'
                else:
                    trial_type='invalid'
            
            trial_tarInDist=0
            
            if thisBlock['cue']=='target':
                if trial_type=='valid': 
                    target_stim.pos= which_circle[0].pos 
                    if blockLat=='bi':
                        if cue_side=='L': 
                            distractor_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos 
                        else:
                            distractor_stim.pos= (np.random.choice(stim_minus_two,1))[0].pos
                    elif blockLat=='uni': #if we have a unilateral cue, we just don't want to put the distractor in the same circle as the target cue, otherwise the pos doesn't matter
                        distractor_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos
                else:  
                    if blockLat=='bi':
                        probe1=np.random.choice(stim_minus_one,1,replace=False) # select one circle from left side and one circle from right side
                        probe2=np.random.choice(stim_minus_two,1,replace=False)
                        probe1=probe1[0]
                        probe2=probe2[0]
                        tarNdist=np.random.choice([probe1,probe2],2,replace=False)
                    elif blockLat=='uni':
                        tarNdist=np.random.choice(stim_minus_one,2,replace=False) #select two circles that aren't the cued circles
                    #then randomly  assign the target to one and dist to another
                    distractor_stim.pos=tarNdist[0].pos 
                    target_stim.pos=tarNdist[1].pos
            
            elif thisBlock['cue']=='distractor':
                if trial_type=='valid': 
                    distractor_stim.pos=which_circle[0].pos
                    if blockLat=='bi':
                        if cue_side=='L':
                            target_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos
                        else:
                            target_stim.pos= (np.random.choice(stim_minus_two,1))[0].pos
                    elif blockLat=='uni':
                        target_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos
                else:
                   if (np.random.choice([True,False],1,p=[.10,.90])[0]): #if the trial's cued location is invalid AND we want a target in a distractor-cued loc
                        #we only want a target in a dist cued loc once in a while (10% of all invalid trials)
                        if blockLat=='bi': #if there are 2 distractor cues
                            tarinDistloc=np.random.choice([cue_target_1[0],cue_target_2[0]],1) #randomly choose the left or right cue to put it in
                            target_stim.pos=tarinDistloc[0].pos #put the target in the chosen 'distractor' circle
                            if tarinDistloc[0]==cue_target_1[0]:
                                cue_side=='R'
                            else:
                                cue_side=='L'
                            if cue_side=='L':
                                distractor_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos #put the distractor on the opposite side of the target
                            else:
                                distractor_stim.pos=(np.random.choice(stim_minus_two,1))[0].pos
                        elif blockLat=='uni':
                            target_stim.pos=cue_target_1[0].pos
                            distractor_stim.pos=np.random.choice(stim_minus_one,1)[0].pos
                        trial_tarInDist=1
                        
                        if EEGflag:
                            port.close()
                            port.open()
                            port.write(startSaveflag)
                            port.flush()
                            core.wait(.2)
                            port.close()
                   else:
                        if blockLat=='bi':
                            probe1=np.random.choice(stim_minus_one,1,replace=False) #select two circles that aren't the cued circles
                            probe2=np.random.choice(stim_minus_two,1,replace=False)
                            tarNdist=np.random.choice([probe1[0],probe2[0]],2,replace=False) #them randomly assign the target to one and dist to another
                            distractor_stim.pos=tarNdist[0].pos 
                            target_stim.pos=tarNdist[1].pos
                        elif blockLat=='uni':
                            probe=np.random.choice(stim_minus_one,2,replace=False)
                            probe1=probe[0]
                            probe2=probe[1]
                            distractor_stim.pos=probe1.pos
                            target_stim.pos=probe2.pos
                            distractor_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the distractor
            distractor_stim.draw()
            target_stim.ori=5
            while target_stim.ori==5 or (target_stim.ori == distractor_stim.ori) or (target_stim.ori+180 == distractor_stim.ori) or (target_stim.ori-180==distractor_stim.ori):
                target_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the target
            target_stim.draw()
            
            if target_stim.ori==0:
                corrKey='up'
            elif target_stim.ori==90:
                corrKey='right'
            elif target_stim.ori==180:
                corrKey='down'
            elif target_stim.ori==270:
                corrKey='left'
            
            for s in range(len(stimuli)): 
                circs=stimuli[s]
                if not (((circs.pos[0]==target_stim.pos[0]) and (circs.pos[1]==target_stim.pos[1])) or ((circs.pos[0]==distractor_stim.pos[0]) and (circs.pos[1]==distractor_stim.pos[1]))): 
                    #if the circle is not a target or distractor then put other_stim in it
                    circs.setLineColor([1,-1,-1]) #if the circle is a non singleton distractor make it red
                    circs.setFillColor(None)
                    redL[s].ori=(np.random.choice([0,90,180,270],1))[0]
                    redL[s].pos=circs.pos
                    redL[s].draw()
                elif (circs.pos[0]==target_stim.pos[0] and circs.pos[1]==target_stim.pos[1]):
                    circs.setLineColor([1,-1,-1]) #if the circle is a target we want it to be red, too
                    circs.setFillColor(None)
                else: #if the circle is a chosen distractor, make it yellow
                    circs.lineColorSpace='rgb255'
                    circs.setLineColor([255,255,0])
                    circs.setFillColor(None)
                    
            win.flip()
            core.wait(2)
            
            fixation.draw()
            for circs in stimuli:
                circs.lineColorSpace='rgb'
                circs.setLineColor([0,0,0])
                circs.setFillColor([0,0,0])
            
            win.flip()
            core.wait(ITI)