# ### MRI adaptation of alpha paradigm -- no distractor condition. 
    # adding the event triggers for MRI ttl
        # 0 deg rotation=6, 90=7,180=8,270=9

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
expName='alpha_pilot'
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
win = visual.Window([1680,1050],units='deg',fullscr=False,monitor='testMonitor',checkTiming=True)
no_stim=6
vis_deg=3.5
flex_cond_flag=0

#redT=visual.ImageStim(win, image='C:\Stimuli\T2.png') 
#redI=visual.ImageStim(win, image='C:\Stimuli\I3.png') #EEG stimulus presentation Dell
#yellowT=visual.ImageStim(win, image='C:\Stimuli\YellowT.png')
#redLpath='C:\Stimuli'
#filename='Z:/AlphaStudy_Data/eegData/eeg_behavior_data'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])
redT=visual.ImageStim(win, image='/Users/dcellier/Documents/GitHub/Alpha-Study/stimuli/T2.png') 
redI=visual.ImageStim(win, image='/Users/dcellier/Documents/GitHub/Alpha-Study/stimuli/I3.png')
yellowT=visual.ImageStim(win, image='/Users/dcellier/Documents/GitHub/Alpha-Study/stimuli/YellowT.png')
redLpath='/Users/dcellier/Documents/GitHub/Alpha-Study/stimuli/'
filename='/Users/Shared/'+u'data/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])
refresh_rate=50 #not sure what the real refresh rate is

#refresh_rate=50
#redL=[visual.ImageStim(win, image=redLpath+'\RedL copy 0.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 1.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 2.png'),
#    visual.ImageStim(win, image=redLpath+'\RedL copy 3.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 4.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 5.png'),
#    visual.ImageStim(win, image=redLpath+'\RedL copy 6.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 7.png'),visual.ImageStim(win, image=redLpath+'\RedL copy 8.png')]

redL=[visual.ImageStim(win, image=redLpath+'RedL copy 0.png'),visual.ImageStim(win, image=redLpath+'RedL copy 1.png'),visual.ImageStim(win, image=redLpath+'RedL copy 2.png'),
    visual.ImageStim(win, image=redLpath+'RedL copy 3.png'),visual.ImageStim(win, image=redLpath+'RedL copy 4.png'),visual.ImageStim(win, image=redLpath+'RedL copy 5.png'),
    visual.ImageStim(win, image=redLpath+'RedL copy 6.png'),visual.ImageStim(win, image=redLpath+'RedL copy 7.png'),visual.ImageStim(win, image=redLpath+'RedL copy 8.png')]

distractor_stim=yellowT
target_stim=redT
other_stim=redL

num_trials=33
num_reps=3 #3

def pracCond(thisBlock,n_practrials=10,demo=False):
    pracDataList=[]
    for n in range(n_practrials):
        ITI=2.0
        # info for this block --for subject ######################################
        if n==0:
            for circs in stimuli:
                circs.opacity = 0 
            #fixation.Autodraw=False
            if demo:
                info_msg3=visual.TextStim(win,pos=[0,0],units='norm',text=thisBlock['cue']+' cue demonstration')
                info_msg3.draw()
            else:
                info_msg3=visual.TextStim(win,pos=[0,0],units='norm',text='Begin practice block')
                info_msg3.draw()
            win.update()
            core.wait(2)
            #fixation.Autodraw=True
            fixation.draw()
            win.flip()
            core.wait(3)# pre-block pause
        for circs in stimuli:
            circs.opacity=1
            circs.setLineColor([0,0,0])
        cue_target_1=np.random.choice(right_stim,1)
        cue_target_2=np.random.choice(left_stim,1)
        color_ind=cue_types_scramble.index(thisBlock['cue'])
        cue_target_1[0].setLineColor(colors_scramble[color_ind])
        cue_target_2[0].setLineColor(colors_scramble[color_ind])
        fixation.draw()
        win.flip()
        core.wait(.5) # CUE PERIOD #################################################
        fixation.draw()
        # ## SOA period
        for circs in stimuli:
            circs.setLineColor([0,0,0])
        win.flip()
        core.wait(1.5) # DELAY #####################################################
        fixation.draw()
        target_loc1 = list(right_stim).index(cue_target_1[0]) #where are the two cued circles?
        stim_minus_one = np.delete(right_stim, target_loc1) 
        target_loc2 = list(left_stim).index(cue_target_2[0]) 
        stim_minus_two = np.delete(left_stim,target_loc2) #get a list of stimuli that don't include cued circles
        which_circle = np.random.choice([cue_target_1[0], cue_target_2[0], stim_minus_two],1,p=[0.5,0.5,0.0])
        if thisBlock['cue']=='neutral':#since the neutral cue is neutral, it isn't going to be valid and targets/distractors will be randomly assigned
            trial_type='n/a'
        elif (which_circle[0] in cue_target_1):
            trial_type='valid'
            cue_side='R'
        elif (which_circle[0] in cue_target_2): #if the dis or target is in one of the circles cued, it was a predictive trial. SAVE OUT this info later!!!!!
            trial_type='valid'
            cue_side='L'
        else:
            trial_type='invalid'
        trial_tarInDist=0
        if thisBlock['cue']=='target':
            if trial_type=='valid': #if this trial's cued locations are valid, put the target in one of them
                target_stim.pos= which_circle[0].pos 
                if cue_side=='L': #if the target is on the Left side of the clock, we want the dist on the right and vice versa
                    distractor_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos
                else:
                    distractor_stim.pos= (np.random.choice(stim_minus_two,1))[0].pos
            else: #if this trial is invalid 
                    tar=np.random.choice(stim_minus_one,1,replace=False) #select two circles that aren't the cued circles
                    dist=np.random.choice(stim_minus_two,1,replace=False)
                    distractor_stim.pos=dist[0].pos #put the distractor in one and the target in the other
                    target_stim.pos=tar[0].pos
        elif thisBlock['cue']=='distractor':
            if trial_type=='valid': #if this trial's cued locations are valid, put the distractor in one of them
                distractor_stim.pos=which_circle[0].pos
                if cue_side=='L': #if the dist is on the Left side of the clock, we want the target on the right and vice versa
                    target_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos
                else:
                    target_stim.pos= (np.random.choice(stim_minus_two,1))[0].pos
            else:
                probe1=np.random.choice(stim_minus_one,1,replace=False) #select two circles that aren't the cued circles
                probe2=np.random.choice(stim_minus_two,1,replace=False)
                tarNdist=np.random.choice([probe1[0],probe2[0]],2,replace=False) #them randomly assign the target to one and dist to another
                distractor_stim.pos=tarNdist[0].pos 
                target_stim.pos=tarNdist[1].pos
        elif thisBlock['cue']=='neutral':
            probe1=np.random.choice(stim_minus_one,1,replace=False) #select two circles that aren't the cued circles
            probe2=np.random.choice(stim_minus_two,1,replace=False)
            tarNdist=np.random.choice([probe1[0],probe2[0]],2,replace=False) #them randomly assign the target to one and dist to another
            distractor_stim.pos=tarNdist[0].pos
            target_stim.pos=tarNdist[1].pos
        distractor_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the distractor
        distractor_stim.opacity=1
        distractor_stim.draw()
        target_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the target
        target_stim.opacity=1
        target_stim.draw()
        if target_stim.ori==0:
            corrKey='6'
        elif target_stim.ori==90:
            corrKey='7'
        elif target_stim.ori==180:
            corrKey='8'
        elif target_stim.ori==270:
            corrKey='9'
        for n in range(len(stimuli)): 
            circs=stimuli[n]
            if not (((circs.pos[0]==target_stim.pos[0]) and (circs.pos[1]==target_stim.pos[1])) or ((circs.pos[0]==distractor_stim.pos[0]) and (circs.pos[1]==distractor_stim.pos[1]))): #if the circle is not a target or distractor then put other_stim in it
                circs.setLineColor([1,-1,-1]) #if the circle is a non singleton distractor make it red
                circs.setFillColor(None)
                redL[n].ori=(np.random.choice([0,90,180,270],1))[0]
                redL[n].pos=circs.pos
                redL[n].opacity=1
                redL[n].draw()
            elif (circs.pos[0]==target_stim.pos[0] and circs.pos[1]==target_stim.pos[1]):
                circs.setLineColor([1,-1,-1]) #if the circle is a target we want it to be red, too
                circs.setFillColor(None)
            else: #if the circle is a chosen distractor, make it yellow
                circs.lineColorSpace='rgb255'
                circs.setLineColor([255,255,0])
                circs.setFillColor(None)
        win.update()
        clock=core.Clock()
        if not demo:
            subResp= event.waitKeys(1.5,keyList=['6','7','8','9'],timeStamped=clock)
            if subResp==None:
                trial_corr=0
            else:
                if subResp[0][0]==corrKey:
                    trial_corr=1
                else:
                    trial_corr=0
        else: 
            core.wait(1.5)
        fixation.draw()
        for circs in stimuli:
            circs.lineColorSpace='rgb'
            circs.setLineColor([0,0,0])
            circs.setFillColor([0,0,0])
        for letter in other_stim:
            letter.opacity=0
        distractor_stim.opacity=0
        target_stim.opacity=0
        if not demo:
            Thistrial_data= trial_corr
            pracDataList.append(Thistrial_data)
        win.flip()
        core.wait(ITI)
        for circs in stimuli:
            circs.opacity=0
    if not demo:
        #fixation.color=([0,0,0])
        acc_feedback=visual.TextStim(win, pos=[0,.5],units='norm',text='Your accuracy for the practice round was %i percent. Practice again? (y/n)' %(100*(np.sum(pracDataList)/n_practrials)))
        acc_feedback.draw()
        win.update()
        cont=event.waitKeys(keyList=['y','n'])
        fixation.color=([1,1,1])
        if cont[0]=='y':
            pracCond(thisBlock,n_practrials)

def wait_here(t):
    interval=1/refresh_rate
    num_frames=int(t/interval)
    for n in range(num_frames): #change back to num_frames
        fixation.draw()
        win.flip()
def make_ITI():
    ITI=np.random.choice([3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6],1)[0] # averages to around 4 seconds?
    return ITI
def make_csv(filename):
    with open(filename+'.csv', mode='w') as csv_file:
        fieldnames=['block','cue','validity','uni or bi lat?','flex or blocked?','trialNum','trial_type','corrResp','subResp','trialCorr?','RT','stim_loc(T,D)','tarinDisCond','ITI']
        #fieldnames is simply asserting the categories at the top of the CSV
        writer=csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writeheader()
        print('\n\n\n')
        for n in range(len(blocks.keys())): # loop through each block
            blocks_data = list(blocks.keys())[n]
            ThisBlock=blocks[blocks_data] #grabbing the block info for this block
            #print(ThisBlock)
            #print('\n')
            for k in range(len(ThisBlock['trialsData'])): #this should be the # of trials
                ThisTrial=ThisBlock['trialsData'][k] #grabbing the trial info out of data for this trial
                #print(ThisTrial)
                writer.writerow({'block':ThisBlock['block'],'cue':ThisBlock['cueType'],'validity':ThisBlock['validity'],
                                'uni or bi lat?':ThisBlock['blockLat'],'flex or blocked?':ThisBlock['blockFlex'],'trialNum':ThisTrial['trialNum'],'trial_type':ThisTrial['trial_type'],
                                'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                'RT':ThisTrial['RT'],'stim_loc(T,D)':ThisTrial['stim_loc'],'tarinDisCond':ThisTrial['tarinDisCond'],
                                'ITI':ThisTrial['ITI']})

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
distractor_stim.opacity=0
target_stim.opacity=0
distractor_stim.autoDraw=True
target_stim.autoDraw=True
for stim in other_stim:
    stim.autoDraw=True
    stim.opacity=0
    stim.size=([1.25,1.25])
fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))
fixation.size=0.6


# #### FLAGS ############################################
twoCue_flag=1 # only bilateral cues, no  unilateral, if this flag is true
flexNblock_flag=1 # both flex and blocked conditions if this flag is true

neutralFlag=1
other=0.95
cue_types=['target']
if neutralFlag:
    cue_types.append('neutral')
    cue_valid=[other]
else:
    chance=(1/6)*2
    cue_valid=[other,chance]
stimList=[]
for cue in ['target','distractor']:
    for num in cue_valid:
        stimList.append({'cue':cue,'validity':num})
if neutralFlag:
    stimList.append({'cue':'neutral','validity':0})

EEGflag=0 # change back to 1
if EEGflag: 
    startSaveflag=bytes([254])
    stopSaveflag=bytes([255])
    #cue_onset_trig=bytes([101])
    tarU3_trig=bytes([111])
    tarB3_trig=bytes([113])
    tarU9_trig=bytes([115])
    tarB9_trig=bytes([117])
    disU3_trig=bytes([119])
    disU9_trig=bytes([121])
    disB3_trig=bytes([123])
    disB9_trig=bytes([125])
    probetrig=bytes([127])
    neutralU_trig=bytes([129])
    neutralB_trig=bytes([131])
    tarinDist_trig=bytes([103])
    subNonRespTrig=bytes([105])
    subRespTrig=bytes([107])
    ITItrig=bytes([109])
    endofBlocktrig=bytes([133])
    port=serial.Serial('COM4',baudrate=115200)
    port.close()

intro_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Welcome to the experiment!')
intro_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='You will see a series of circles that will indicate the location of the target "T" or of the distractor "I" some portion of the time')
intro_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Press any key to continue')
intro_msg.draw()
intro_msg2.draw() 
intro_msg3.draw()
win.flip()
event.waitKeys()
intro_mesg4= visual.TextStim(win,pos=[0,.5],units='norm',text='Please remain focused on the cross in the middle of the screen whenever there are NOT circles on the screen.')
intro_mesg5=visual.TextStim(win,pos=[0,0], units='norm',text='Respond to the orientation of the capital "T" using the arrow keys on the keyboard')
intro_mesg6=visual.TextStim(win,pos=[0,-0.5],units='norm',text='You will also see a capital "I." Do NOT respond to the orientation of the I. Press any key to continue.')
intro_mesg4.draw()
intro_mesg5.draw()
intro_mesg6.draw()
win.flip()
event.waitKeys()
win.flip()

blocks={}
if EEGflag:
    port.open()
    #win.callonFlip(pport.setData,delay1trig)
    port.write(startSaveflag)
    port.close()

order=np.random.choice(len(cue_types),len(cue_types),replace=False) # num of conds in cue_types #this is randomly coming up with the indices of the conds in the scrambled list
cue_types_scramble=np.zeros((len(cue_types))) 
colors_scramble=np.zeros((len(cue_types)))
cues=cue_types[:] #yields ['target','distractor'] so that the following for loop can select these and insert them into cue_types_scramble
if neutralFlag:
    colors=([-1,1,-1],[0,0,1],[1,1,0])
else:
    colors=([-1,-1,1],[-1,1,-1]) 
order=list(order)
cue_types_scramble=list(cue_types_scramble)
colors_scramble=list(colors_scramble)
for ind in order:
    cue_types_scramble[ind]=cues[order.index(ind)]
    colors_scramble[ind]=colors[order.index(ind)]

if twoCue_flag:
    lattypes=['bi']
else:
    lattypes=['bi','uni']
if flexNblock_flag:
    cue_changes=['flex','blocked']
else:
    cue_changes=['flex']

print(cue_types_scramble)

if EEGflag:
    port.open()

k=0
for cue in cue_types_scramble: #looping through the types of cues in sequence, since we care about the order now. 
    
    if cue != 'neutral':
        cue_VnL=[] #here, we're initiating a list of the validities and the lateralizations (bilateral or unilateral) and pairing them for however many times they need to be carried out (2)
        for c in cue_valid:
            for lattype in lattypes: #['bi','uni']:
                for v in cue_changes:
                    for n in range(num_reps):
                        cue_VnL.append([c,lattype,v])
    else:
        cue_VnL=[]
        for lattype in lattypes:
            for v in cue_changes:
                for n in range(num_reps):
                    cue_VnL.append([0,lattype,v])
    order2=np.random.choice(len(cue_VnL),len(cue_VnL),replace=False) #this is going to be the order that we ultimately call ea of the conditions in
    order2=list(order2)
    cue_VnL_scramble=np.zeros((len(cue_VnL)))
    cue_VnL_scramble=list(cue_VnL_scramble)
    for ind2 in order2:
        cue_VnL_scramble[ind2]=cue_VnL[order2.index(ind2)]
    print(cue_VnL_scramble)
    
    reps=len(cue_VnL_scramble)
    
    for block in (range(reps)): #we want each cue type to repeat (num_reps * the # of validity conds * 2 laterality conds) times 
        
        blockFlex=cue_VnL_scramble[block][2]
        blockLat=cue_VnL_scramble[block][1]
        thisValid=cue_VnL_scramble[block][0]
        trialDataList=[]
        thisBlock=stimList[stimList.index({'cue':cue,'validity':thisValid})]
        
        for n in range(num_trials):
            ITI=make_ITI()
            
            if n==0 and block==0:
                for circs in stimuli:
                    circs.opacity = 0 
                pracCond(thisBlock=thisBlock,demo=True)
                pracCond(thisBlock=thisBlock,demo=False)
                fixation.autoDraw=True
                fixation.opacity=0
            if n==0:
                fixation.color=([0,0,0])
                info_msg=visual.TextStim(win, pos=[0,.5],units='norm',text='This block will show %s cues' %thisBlock['cue']) 
                info_msg.draw()
                info_msg2=visual.TextStim(win, pos=[0,-.5], units='norm',text='Press any key to continue')
                info_msg2.draw()
                win.update()
                key1=event.waitKeys()
                fixation.autoDraw=False
                MRI_wait=visual.TextStim(win, pos=[0,.5], units='norm', text='Please wait for scanner...') 
                MRI_wait.draw()
                win.flip()
                event.waitKeys(keyList=['^','z'])
                #win.flip()
                fixation.autoDraw=True
                fixation.color=([1,1,1])
                win.flip() 
                core.wait(3)# pre-block pause
            
            for circs in stimuli:
                circs.opacity=1
                circs.setLineColor([0,0,0])
                circs.setFillColor([0,0,0])
             
            if (blockFlex=='blocked' and n==0) or (blockFlex=='flex'):
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
                if thisBlock['cue']=='target':
                    if thisBlock['validity']==other:
                        if blockLat=='bi':
                            thistrialFlag=tarB9_trig
                        elif blockLat=='uni':
                            thistrialFlag=tarU9_trig
                    elif thisBlock['validity']==chance:
                        if blockLat=='bi':
                            thistrialFlag=tarB3_trig
                        elif blockLat=='uni':
                            thistrialFlag=tarU3_trig
                elif thisBlock['cue']=='distractor':
                    if thisBlock['validity']==other:
                        if blockLat=='bi':
                            thistrialFlag=disB9_trig
                        elif blockLat=='uni':
                            thistrialFlag=disU9_trig
                    elif thisBlock['validity']==chance:
                        if blockLat=='bi':
                            thistrialFlag=disB3_trig
                        elif blockLat=='uni':
                            thistrialFlag=disU3_trig
                elif thisBlock['cue']=='neutral':
                    if blockLat=='uni':
                        thistrialFlag=neutralU_trig
                    elif blockLat=='bi':
                        thistrialFlag=neutralB_trig
            
            if EEGflag:
                win.callOnFlip(port.write,thistrialFlag)
            
            wait_here(.5) # ############## Cue presentation ###################
            
            fixation.draw()
            for circs in stimuli:
                circs.setLineColor([0,0,0])
            
            wait_here(1.5) # ############ delay one/SOA period ###############
            
            fixation.draw()
            
            odds=thisBlock['validity']
            
            if not thisBlock['cue']=='neutral':
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
                                cue_side='R'
                            else:
                                cue_side='L'
                            if cue_side=='L':
                                distractor_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos #put the distractor on the opposite side of the target
                            else:
                                distractor_stim.pos=(np.random.choice(stim_minus_two,1))[0].pos
                        elif blockLat=='uni':
                            target_stim.pos=cue_target_1[0].pos
                            distractor_stim.pos=np.random.choice(stim_minus_one,1)[0].pos
                        trial_tarInDist=1
                        if EEGflag:
                            port.write(tarinDist_trig)
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
            
            elif neutralFlag and thisBlock['cue']=='neutral':
                if blockLat=='bi':
                    probe1=np.random.choice(right_stim,1,replace=False) #select two circles, one on left and one on right
                    probe2=np.random.choice(left_stim,1,replace=False)
                    tarNdist=np.random.choice([probe1[0],probe2[0]],2,replace=False) #them randomly assign the target to one and dist to another
                    distractor_stim.pos=tarNdist[0].pos 
                    target_stim.pos=tarNdist[1].pos
                    # want to document if any of the randomly assigned circles match the cued circles
                    if ((distractor_stim.pos[0]==cue_target_1[0].pos[0] and distractor_stim.pos[1]==cue_target_1[0].pos[1]) or (distractor_stim.pos[0]==cue_target_2[0].pos[0] and distractor_stim.pos[1]==cue_target_2[0].pos[1])) and ((target_stim.pos[0]==cue_target_1[0].pos[0] and target_stim.pos[1]==cue_target_1[0].pos[1]) or (target_stim.pos[0]==cue_target_2[0].pos[0] and target_stim.pos[1]==cue_target_2[0].pos[1])):
                        trial_type='bothvalid' #if they somehow happen to both be assigned a distractor and a target, both cues are valid
                    elif (target_stim.pos[0]==cue_target_1[0].pos[0] and target_stim.pos[1]==cue_target_1[0].pos[1]) or (target_stim.pos[0]==cue_target_2[0].pos[0] and target_stim.pos[1]==cue_target_2[0].pos[1]):
                        trial_type='Tvalid' #if the target is assigned to one of the cue'd location, the cue was valid for the target
                    elif (distractor_stim.pos[0]==cue_target_1[0].pos[0] and distractor_stim.pos[1]==cue_target_1[0].pos[1]) or (distractor_stim.pos[0]==cue_target_2[0].pos[0] and distractor_stim.pos[1]==cue_target_2[0].pos[1]):
                        trial_type='Dvalid' #and vice versa for distractor
                    else: 
                        trial_type='invalid' # else, the cues were entirely unhelpful
                elif blockLat=='uni':
                    tarNdist=np.random.choice(stimuli,2,replace=False)
                    distractor_stim.pos=tarNdist[0].pos
                    target_stim.pos=tarNdist[1].pos
                    if (distractor_stim.pos[0]==cue_target_1[0].pos[0] and distractor_stim.pos[1]==cue_target_1[0].pos[1]):
                        trial_type='Dvalid'
                    elif (target_stim.pos[0]==cue_target_1[0].pos[0] and target_stim.pos[1]==cue_target_1[0].pos[1]):
                        trial_type-'Tvalid'
                    else:
                        trial_type='invalid'
            
            distractor_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the distractor
            distractor_stim.opacity=1
            distractor_stim.draw()
            target_stim.ori=5
            while target_stim.ori==5 or (target_stim.ori == distractor_stim.ori) or (target_stim.ori+180 == distractor_stim.ori) or (target_stim.ori-180==distractor_stim.ori):
                target_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the target
            target_stim.opacity=1
            target_stim.draw()
            
            if target_stim.ori==0:
                corrKey='6'
            elif target_stim.ori==90:
                corrKey='7'
            elif target_stim.ori==180:
                corrKey='8'
            elif target_stim.ori==270:
                corrKey='9'
            
            for s in range(len(stimuli)): 
                circs=stimuli[s]
                if not (((circs.pos[0]==target_stim.pos[0]) and (circs.pos[1]==target_stim.pos[1])) or ((circs.pos[0]==distractor_stim.pos[0]) and (circs.pos[1]==distractor_stim.pos[1]))): 
                    #if the circle is not a target or distractor then put other_stim in it
                    #circs.setLineColor([255,255,0],colorSpace='rgb255')
                    circs.setLineColor([1,-1,-1]) #if the circle is a non singleton distractor make it red
                    circs.setFillColor(None)
                    redL[s].ori=(np.random.choice([0,90,180,270],1))[0]
                    redL[s].pos=circs.pos
                    redL[s].opacity=1
                    redL[s].draw()
                elif (circs.pos[0]==target_stim.pos[0] and circs.pos[1]==target_stim.pos[1]):
                    circs.setLineColor([1,-1,-1]) #if the circle is a target we want it to be red, too
                    circs.setFillColor(None)
                else: #if the circle is a chosen distractor, make it yellow
                    circs.lineColorSpace='rgb255'
                    circs.setLineColor([255,255,0])
                    circs.setFillColor(None)
            #win.update()
            
#            t=2
#            interval=1/refresh_rate
#            num_frames=int(t/interval)
            
            if EEGflag:
                # port.flush()
                win.callOnFlip(port.write,probetrig)
#            if EEGflag:
#                port.open()
            
            #wait_here(2) # ############### probe presentation ####################
            
            event.clearEvents()
            max_win_count=int(2/(1/refresh_rate))
            win_count=0
            subResp=None
            clock=core.Clock()
            while not subResp:
                win.flip()
                subResp=event.getKeys(keyList=['6','7','8','9'], timeStamped=clock)
                win_count=win_count+1
                if win_count==max_win_count:
                    break
            
            if not subResp:
                if EEGflag:
                    port.write(subNonRespTrig)
                trial_corr=np.nan
                RT=np.nan
                key='None'
            else:
                if EEGflag:
                    port.write(subRespTrig)
                if subResp[0][0]==corrKey:
                    trial_corr=1
                else:
                    trial_corr=0
                RT=subResp[0][1]
                key=subResp[0][0]
            
            fixation.draw()
            for circs in stimuli:
                circs.lineColorSpace='rgb'
                circs.setLineColor([0,0,0])
                circs.setFillColor([0,0,0])
            for circs in other_stim:
                circs.opacity=0
            target_stim.opacity=0
            distractor_stim.opacity=0
            
            win.flip()
            #core.wait(ITI)
            
            for stim in stimuli:
                if (stim.pos[0]==target_stim.pos[0]) and (stim.pos[1]==target_stim.pos[1]):
                    target_circle=stim
                elif (stim.pos[0]==distractor_stim.pos[0]) and (stim.pos[1]==distractor_stim.pos[1]):
                    distractor_circle=stim
                else:
                    continue
            
            Thistrial_data= {'trialNum':(n+1),'trial_type':trial_type,'corrResp':corrKey,'subjectResp':key,'trialCorr?':trial_corr,'RT':RT, 'stim_loc':(target_circle.name,distractor_circle.name),'tarinDisCond':trial_tarInDist,'ITI':ITI}
            trialDataList.append(Thistrial_data)
            
            print(trialDataList)
            
            key=event.getKeys()
            if key: 
                if key[0]=='escape': 
                    win.close()
                    core.quit()
                    print('FORCED QUIT')
            
            if EEGflag:
                win.callOnFlip(port.write,ITItrig)
            
            #core.wait(ITI) #ITI--want to jitter this?, with an average of 4 seconds
            wait_here(ITI)
#            port.close()
#            
        blocks.update({'blockInfo_%i%s'%(block,cue):{'block':k,'cueType':thisBlock['cue'],'validity':thisBlock['validity'],'blockLat':blockLat,'blockFlex':blockFlex,'trialsData':trialDataList}})
        # #########################saving data out###########################################
        make_csv(filename)
        if EEGflag:
            port.write(endofBlocktrig)
        
        k=k+1
        
    exit_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='You are finished with this cue type!')
    exit_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Please call the experimenter in for further instruction')
    exit_msg.draw() 
    exit_msg3.draw()
    win.flip()
    event.waitKeys(keyList=['q'])

if EEGflag:
    port.write(stopSaveflag)
    port.close()

exit_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Thank you for participating in our experiment!')
exit_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='Your time and cooperation is greatly appreciated.')
exit_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Press any key to exit')
exit_msg.draw()
exit_msg2.draw() 
exit_msg3.draw()

win.flip()
event.waitKeys()