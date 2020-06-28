## Singleton search paradigm, collaboration w Shaun Vecera & Brad Stilwell
# updates 05/08/19: changing paradigm so that target shape and target color changes trial-to-trial, and so that vis_deg is closer to central fixation 

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,

                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,

                   sqrt, std, deg2rad, rad2deg, linspace, asarray)

from numpy.random import random, randint, normal, shuffle,uniform,permutation
import os  # handy system and path functions
import sys  # to get file system encoding
import serial #for sending triggers from this computer to biosemi computer
import csv
import copy
from psychopy import visual, core

expInfo = {'subject': '', 'session': '01','EEG? [y/n]':'n','refresh':50}
expName='alpha_singleton_pilot'
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
win = visual.Window([1680,1050],units='deg',fullscr=True,monitor='testMonitor',checkTiming=True)
no_stim=6
vis_deg=4.2#3.5#*10


for key in ['escape']:
    event.globalKeys.add(key, func=core.quit)
    


if expInfo['EEG? [y/n]']=='y':
    EEGflag=1
else:
    EEGflag=0

if EEGflag:
    port=serial.Serial('COM4',baudrate=115200)
    port.close()
    startSaveflag=bytes([254])
    stopSaveflag=bytes([255])
    #cue_onset_trig=bytes([101])
    
    cue_possibilities=['neut','dis']
    
    cue_trigDict={}
    trig_num=101
    for c in cue_possibilities:
        label=c+'_trig'
        trig=trig_num
        cue_trigDict[label]=trig
        trig_num+=2 #setting it up so that it increases by every odd number after 101
     
    probe_trigDict={}
    if trig_num == 101:
        print('oops, the cue_trigDict did not work')
        core.quit()
    
    dis_possibilities=['neutA','neutP','disP']
    trig_num=trig_num+2
    for d in dis_possibilities:
        label=d+'_trig'
        trig=trig_num
        probe_trigDict[label]=trig
        trig_num+=2
    
    subNonRespTrig=bytes([trig_num+2])
    subRespTrig=bytes([trig_num+4])
    ITItrig=bytes([trig_num+6])
    endofBlocktrig=bytes([trig_num+8])
    
    other_trigDict={'startSaveflag':startSaveflag,'stopSaveflag':stopSaveflag,'ITItrig':ITItrig,'endofBlocktrig':endofBlocktrig}
    #cue_trigDict={'HHP_trig':HHP_trig,'HLP_trig':HLP_trig,'HHA_trig':HHA_trig,'HLA_trig':HLA_trig,
    #        'NLP_trig':NLP_trig,'NLA_trig':NLA_trig,'NHP_trig':NHP_trig,'NHA_trig':NHA_trig}
    #probe_trigDict={'tarVdisVH_trig':tarVdisVH_trig,'tarVdisVL_trig':tarVdisVL_trig,
    #        'tarNdisVH_trig':tarNdisVH_trig,'tarNdisVL_trig':tarNdisVL_trig,'tarVdisIH_trig':tarVdisIH_trig,'tarVdisIL_trig':tarVdisIL_trig,'tarNdisIH_trig':tarNdisIH_trig,
    #        'tarNdisIL_trig':tarNdisIL_trig}
    response_trigDict={'subNonRespTrig':subNonRespTrig,'subRespTrig':subRespTrig}
    print(cue_trigDict)
    print(probe_trigDict)
    print(other_trigDict)
    print(response_trigDict)

if EEGflag:
    filename='Z:/AlphaStudy_Data/eegData/eeg_behavior_data'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])
else:
    filename='Z:/AlphaStudy_Data/behavData'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date']) #for dells
    #filename='/Volumes/rdss_kahwang/AlphaStudy_Data/behavData'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])

refresh_rate=expInfo['refresh']

num_trials=48 #has to be even number, divisible by 4 (so 1/4 neutral-absent and 1/4 neutral-present)
num_blocks=5

#trialNum':(n),'tarVorI':tarVorI,'disCue_type':disCue_type,'dPOA':dPOA,'disVorI':disVorI,'distractor_loc':loc,'corrResp':corrKey
#blocks.update({'blockInfo_%i'%(block):{'block':block,'tarCue':thisBlock[0],'disCue':thisBlock[1],'highProbLoc?':disProb,'likely_dis':saveDis,'likelyDisHemisphere':disHemi,'trialsData':trialDataList}})

def pracCond(n_practrials=8,demo=False):
    pracDataList=[]
    pracBlock=[]
    for r in range(int(n_practrials/2)):
        pracBlock.append('dis')
        pracBlock.append('neut')
    for n in range(n_practrials):
        ITI=2.0
        distractor_stim,target_stim,other_stim,other_name=generate_target()
        if n==0:
            if demo:
                prac_msg=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to begin a demo!')
                prac_msg.draw()
                win.flip()
                event.waitKeys()
            elif not demo:
                prac_msg=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to begin the practice')
                prac_msg.draw()
                win.flip()
                event.waitKeys()
        for circs in stimuli:
            circs.opacity=1
            circs.setLineColor([0,0,0])
            circs.setFillColor([0,0,0])
            circs.size=(circs.size[0]/3,circs.size[1]/3)
            circs.pos=(circs.pos[0]/3,circs.pos[1]/3)
            circs.autoDraw=True
        if pracBlock[n]=='neut':
            cue_circ=list(np.random.choice(stimuli,6,replace=False))
            for c in cue_circ:
                c.setLineColor([1,1,1])
        elif pracBlock[n]=='dis':
            cue_circ=np.random.choice(stimuli,1)
            cue_circ[0].setLineColor([1,1,1])
        fixation.autoDraw=True
        wait_here(1) # ############## Cue presentation ###################
        fixation.autoDraw=True
        for circs in stimuli:
            circs.autoDraw=False
            circs.setLineColor([0,0,0],colorSpace='rgb')
            circs.pos=(circs.pos[0]*3,circs.pos[1]*3)
            circs.size=(circs.size[0]*3,circs.size[1]*3)
        wait_here(1.5) # ############ delay one/SOA period ###############
        if pracBlock[n]=='dis':
            cue_loc=list(stimuli).index(cue_circ[0]) #index of the distractor cue circle
            stim_minus_cue=np.delete(stimuli, cue_loc) #get a list of circles that don't include the distractor cue circ
            which_circle=np.random.choice(stim_minus_cue,1)[0] # choose the target loc
            distractor_stim_clock=(cue_circ[0].pos[0],cue_circ[0].pos[1])
            distractor_stim.pos=(distractor_stim_clock[0],distractor_stim_clock[1])
            distractor_stim.autoDraw=True
        elif pracBlock[n]=='neut': 
            which_circle=np.random.choice(stimuli,1)[0]
            if not demo:
                disAorP='P'
            elif demo:
                disAorP=np.random.choice(['A','P'],1)[0]
            if disAorP=='P':
                tar_loc=list(stimuli).index(which_circle)
                stim_minus_tar=np.delete(stimuli,tar_loc)
                distractor_stim_clock=np.random.choice(stim_minus_tar,1)[0].pos
                distractor_stim.pos=(distractor_stim_clock[0],distractor_stim_clock[1])
                distractor_stim.autoDraw=True
        target_stim.pos=(which_circle.pos[0],which_circle.pos[1])
        target_stim.autoDraw=True
        for s in range(len(stimuli)):
            circs=stimuli[s]
            bars[s].pos=other_stim[s].pos #except target and distractor
            bars[s].ori=(np.random.choice([0,90],1))[0]
            bars[s].autoDraw=True
            if not ((circs.pos[0]==which_circle.pos[0]) and (circs.pos[1]==which_circle.pos[1])):  # if this position isn't the target
                if ((pracBlock[n]=='neut' and disAorP=='P') or pracBlock[n]=='dis'): #if this trial has a distractor 
                    if not ((circs.pos[0]==distractor_stim_clock[0]) and (circs.pos[1]==distractor_stim_clock[1])): # and if this position is also not the distractor
                        #if the circle is not a target or distractor then put other_stim in it
                        other_stim[s].autoDraw=True
                else:
                    other_stim[s].autoDraw=True
            elif ((circs.pos[0]==which_circle.pos[0]) and (circs.pos[1]==which_circle.pos[1])): # if it is the target position
                target_ori=bars[s].ori #then document the orientation of the bar at this loc
                print(target_ori)
        if target_ori==0:
            corrKey='up'
        elif target_ori==90:
            corrKey='left'
#        elif target_ori==180:
#            corrKey='down'
#        elif target_ori==270:
#            corrKey='left'
        #wait_here(2) # ############### probe presentation ####################
        event.clearEvents()
        max_win_count=int(2/(1/refresh_rate))
        win_count=0
        subResp=None
        clock=core.Clock()
        while not subResp:
            win.flip()
            subResp=event.getKeys(keyList=['up','left'], timeStamped=clock)
            win_count=win_count+1
            if win_count==max_win_count:
                break
        if not subResp:
            trial_corr=0
            RT=np.nan
            key='None'
        else:
            if subResp[0][0]==corrKey:
                trial_corr=1
            else:
                trial_corr=0
            RT=subResp[0][1]
            key=subResp[0][0]
        pracDataList.append(trial_corr)
        fixation.draw()
        for circs in stimuli:
            circs.lineColorSpace='rgb'
            circs.setLineColor([0,0,0])
            circs.setFillColor([0,0,0])
        for shape in other_stim:
            shape.autoDraw=False
        for bar in bars:
            bar.autoDraw=False
        target_stim.autoDraw=False
        distractor_stim.autoDraw=False
        win.flip()
        core.wait(ITI)
    if not demo:
        #fixation.color=([0,0,0])
        acc_feedback=visual.TextStim(win, pos=[0,.5],units='norm',text='Your accuracy for the practice round was %i percent. Practice again? (y/n)' %(100*(np.sum(pracDataList)/n_practrials)))
        acc_feedback.draw()
        win.update()
        cont=event.waitKeys(keyList=['y','n'])
        if cont[0]=='y':
            pracCond(n_practrials)
 
def wait_here(t):
    interval=1/refresh_rate
    num_frames=int(t/interval)
    for n in range(num_frames): #change back to num_frames
        fixation.draw()
        win.flip()

def make_ITI():
    if not EEGflag:
        ITI=np.random.choice([1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6],1)[0] #averages to around 2 second?
    else:
        ITI=np.random.choice([3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6],1)[0] # averages to around 4 seconds?
    return ITI

def make_csv(filename,expStart=False):
    with open(filename+'.csv', mode='w') as csv_file:
        #'trialNum':(trial),'trial_type':thisBlock,'dis_type':neutCue_type,'corrResp':corrKey,'subjectResp':key,'trialCorr?':trial_corr,'RT':RT, 'stim_loc':stim_loc,'ITI':ITI,'trial_trigs':(thistrialFlag,probetrig,resp_trig)
        fieldnames=['block','trialNum','trial_type','dis_PresentorAbsent','corrResp','subResp','trialCorr?','RT','stim_loc(T,D)','ITI','Tar,Dis,Other','trial_trigs','triggers']
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
                
                if EEGflag and expStart==True and k==0:
                    writer.writerow({'block':ThisBlock['block'],'trialNum':ThisTrial['trialNum'],'trial_type':ThisTrial['trial_type'],
                                    'dis_PresentorAbsent':ThisTrial['dis_type'],'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                    'RT':ThisTrial['RT'],'stim_loc(T,D)':ThisTrial['stim_loc'],
                                    'ITI':ThisTrial['ITI'],'Tar,Dis,Other':ThisTrial['Tar,Dis,Other'],'trial_trigs':ThisTrial['trial_trigs'],'triggers':(cue_trigDict,probe_trigDict,response_trigDict,other_trigDict)})
                else:
                    writer.writerow({'block':ThisBlock['block'],'trialNum':ThisTrial['trialNum'],'trial_type':ThisTrial['trial_type'],
                                    'dis_PresentorAbsent':ThisTrial['dis_type'],'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                    'RT':ThisTrial['RT'],'stim_loc(T,D)':ThisTrial['stim_loc'],
                                    'ITI':ThisTrial['ITI'],'Tar,Dis,Other':ThisTrial['Tar,Dis,Other'],'trial_trigs':ThisTrial['trial_trigs'],'triggers':''})
if no_stim==6:
    one_oclock = visual.Circle(
    
            win=win, name='1',
    
            size=(0.09, 0.15),
    
            ori=0, pos=((vis_deg/2), (sqrt(3)/2*vis_deg)),
    
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

size=(3.2,2.5) #(.2,.2)
images={'blue_diamond':visual.ImageStim(win=win,name='blue_diamond', units='deg', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/blue_diamond_eq.png'),
    'red_diamond':visual.ImageStim(win=win,name='red_diamond', units='deg', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/red_diamond_eq.png'),
    'yellow_diamond':visual.ImageStim(win=win,name='yellow_diamond', units='deg', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/yellow_diamond_eq.png'),
    'blue_circle':visual.ImageStim(win=win,name='blue_circle', units='deg', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/blue_circle_eq.png'),
    'red_circle':visual.ImageStim(win=win,name='red_circle', units='deg', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/red_circle_eq.png'),
    'yellow_circle':visual.ImageStim(win=win,name='yellow_circle', units='deg', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/yellow_circle_eq.png')}
images_names=list(images.keys())

def generate_target():
    
    distractor_name=np.random.choice(images_names,1)[0]
    if 'blue' in distractor_name:
        target_color=np.random.choice(['red','yellow'],1)[0]
    elif 'yellow' in distractor_name:
        target_color=np.random.choice(['red','blue'],1)[0]
    elif 'red' in distractor_name:
        target_color=np.random.choice(['blue','yellow'],1)[0]
    
    if 'circle' in distractor_name:
        target_shape='diamond'
        other_shape='circle'
    elif 'diamond' in distractor_name:
        target_shape='circle'
        other_shape='diamond'
    
    distractor_stim=images[distractor_name]
    target_stim=images[target_color+'_'+target_shape]
    other_name=target_color+'_'+other_shape
    other_stim=[visual.ImageStim(win=win,image=images[other_name].image, units='deg',ori=0,size=size,name=other_name) for i in range(no_stim)] # making 4 copies of Other_shape 
    for g in range(no_stim):
        #other_stim[g].autoDraw=True
        other_stim[g].pos=(stimuli[g].pos[0],stimuli[g].pos[1])#(stimuli[g].pos[0]/6,stimuli[g].pos[1]/6)#
        #print(stimuli[g].pos)
    
    print(target_stim.name)
    print(distractor_stim.name)
    print(other_stim[0].name)
    
    for stim in stimuli:
        stim.size=(1.5,1.5)
        stim.lineWidth=5
        #stim.pos=(stim.pos[0],stim.pos[1])
    
    distractor_stim.opacity=1
    target_stim.opacity=1
    #distractor_stim.autoDraw=True
    #target_stim.autoDraw=True
    return distractor_stim,target_stim,other_stim,other_name

fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))
fixation.size=0.6

disc_bar= visual.TextStim(win, text='|',units='deg', color=(1,1,1))
disc_bar.size=0.5
bars=[copy.copy(disc_bar) for i in range(no_stim)]

intro_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Welcome to the experiment!')
intro_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='You will see a series circles, then a series of shapes. You must find the shape that is unique. This is the target shape.')#You must find the target shape. The target shape is the %s' % (target_stim.name.split('_')[0])+' '+(target_stim.name.split('_')[1]))
intro_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Press any key to continue')
intro_msg.draw()
intro_msg2.draw() 
intro_msg3.draw()
win.flip()
event.waitKeys()
intro_mesg4= visual.TextStim(win,pos=[0,.6],units='norm',text='Please remain focused on the cross in the middle of the screen whenever there are NOT circles on the screen.')
intro_mesg5=visual.TextStim(win,pos=[0,0], units='norm',text='Respond to the orientation of the line in the target shape using the arrow keys on the keyboard')
intro_mesg6=visual.TextStim(win,pos=[0,-0.6],units='norm',text='You will also sometimes see a distracting shape. The circles help you know where the distracting shape will be. Press any key to continue.')
intro_mesg4.draw()
intro_mesg5.draw()
intro_mesg6.draw()
win.flip()
event.waitKeys()

#targetlist=['tarH','tarN']
cue_list=['dis','neut'] 

stimList=[] #list of trials
for c in cue_list:
    for n in range(int(num_trials/len(cue_list))):
        stimList.append(c)

stimList_blocks=[] #list of blocks, which contains a list of trials
for n in range(num_blocks): 
    stimList_scramble=list(np.random.permutation(stimList))
    stimList_blocks.append(stimList_scramble)

if EEGflag:
    port.open()
    #win.callonFlip(pport.setData,delay1trig)
    port.write(startSaveflag)
    #port.close()

blocks={} # where we will save out the data
likely_dis= np.random.choice(stimuli,1)[0]

pracCond(n_practrials=4,demo=True)
pracCond(n_practrials=8,demo=False)

for block in range(len(stimList_blocks)):
    
    trialDataList=[]
    
    fixation.color=([0,0,0])
    if block !=0:
        info_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to continue to the next block')
    else:
        info_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to begin experiment')
    info_msg2.draw()
    win.flip()
    key1=event.waitKeys()
    fixation.color=([1,1,1])
    fixation.text='+'
    fixation.draw()
    win.flip() 
    core.wait(3)# pre-block pause
    thisBlock=stimList_blocks[block]
    
    neutCue=[]
    for r in range(int(len(thisBlock)/4)): # want 1/4 each of present and absent so that it'll = 1/2 of total trials
        neutCue.append('P')
        neutCue.append('A')
    # we assign these to each neutral trial by calling this list and popping off the P's or A's until the end of the loop
    
    print(thisBlock)
    neutCue_scramble=list(np.random.permutation(neutCue))
    #print(disCue_scramble)
    
    for trial in range(len(thisBlock)):
        distractor_stim,target_stim,other_stim,other_name=generate_target()
        ITI=make_ITI()
        
        print(thisBlock[trial])
        for circs in  stimuli:
            circs.opacity=1
            circs.setLineColor([0,0,0])
            circs.setFillColor([0,0,0])
            circs.size=(circs.size[0]/3,circs.size[1]/3)
            circs.pos=(circs.pos[0]/3,circs.pos[1]/3) #(circs.pos[0]/3,circs.pos[1]/3)
            circs.autoDraw=True
        
        if thisBlock[trial]=='neut':
            cue_circ=list(np.random.choice(stimuli,6,replace=False))
            for c in cue_circ:
                c.setLineColor([1,1,1])
        elif thisBlock[trial]=='dis':
            cue_circ=np.random.choice(stimuli,1)
            cue_circ[0].setLineColor([1,1,1])
            
        fixation.autoDraw=True
        
        if EEGflag:
            thistrialFlag=cue_trigDict[thisBlock[trial]+'_trig']
            win.callOnFlip(port.write,bytes([thistrialFlag]))
        
        wait_here(1) # ############## Cue presentation ###################
        
        fixation.autoDraw=True
        for circs in stimuli:
            circs.setLineColor([0,0,0],colorSpace='rgb')
            circs.pos=(circs.pos[0]*3,circs.pos[1]*3) #(circs.pos[0]*3,circs.pos[1]*3)
            circs.size=(circs.size[0]/3,circs.size[1]/3)
            circs.autoDraw=False
        
        wait_here(1.5) # ############ delay one/SOA period ###############
        
        if thisBlock[trial]=='dis':
            cue_loc=list(stimuli).index(cue_circ[0]) #index of the distractor cue circle
            stim_minus_cue=np.delete(stimuli, cue_loc) #get a list of circles that don't include the distractor cue circ
            which_circle=np.random.choice(stim_minus_cue,1)[0] # choose the target loc
            distractor_stim_clock=(cue_circ[0].pos[0],cue_circ[0].pos[1])
            distractor_stim.pos=(distractor_stim_clock[0],distractor_stim_clock[1])#(distractor_stim_clock[0]/6,distractor_stim_clock[1]/6)
            distractor_stim.autoDraw=True
            disAorP='P'
        elif thisBlock[trial]=='neut': 
            which_circle=np.random.choice(stimuli,1)[0]
            disAorP=neutCue_scramble.pop()
            if disAorP=='P':
                tar_loc=list(stimuli).index(which_circle)
                stim_minus_tar=np.delete(stimuli,tar_loc)
                distractor_stim_clock=np.random.choice(stim_minus_tar,1)[0].pos
                distractor_stim.pos=(distractor_stim_clock[0],distractor_stim_clock[1])#(distractor_stim_clock[0]/6,distractor_stim_clock[1]/6)
                distractor_stim.autoDraw=True
        
        target_stim.pos=(which_circle.pos[0],which_circle.pos[1])#(which_circle.pos[0]/6,which_circle.pos[1]/6)
        target_stim.autoDraw=True
        
        #distractor_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the distractor
        for s in range(len(stimuli)):
            circs=stimuli[s]
            bars[s].pos=other_stim[s].pos #except target and distractor
            bars[s].ori=(np.random.choice([0,90],1))[0]
            bars[s].autoDraw=True
            if not ((circs.pos[0]==which_circle.pos[0]) and (circs.pos[1]==which_circle.pos[1])):  # if this position isn't the target
                if ((thisBlock[trial]=='neut' and disAorP=='P') or thisBlock[trial]=='dis'): #if this trial has a distractor 
                    if not ((circs.pos[0]==distractor_stim_clock[0]) and (circs.pos[1]==distractor_stim_clock[1])): # and if this position is also not the distractor
                        #if the circle is not a target or distractor then put other_stim in it
                        other_stim[s].autoDraw=True
                else:
                    other_stim[s].autoDraw=True
            elif ((circs.pos[0]==which_circle.pos[0]) and (circs.pos[1]==which_circle.pos[1])): # if it is the target position
                target_ori=bars[s].ori #then document the orientation of the bar at this loc
                print(target_ori)
        
        if target_ori==0:
            corrKey='up'
        elif target_ori==90:
            corrKey='left'
        #elif target_ori==180:
#            corrKey='down'
#        elif target_ori==270:
#            corrKey='left'
        
        if EEGflag:
                # port.flush()
                probetrig=probe_trigDict[thisBlock[trial]+disAorP+'_trig']
                win.callOnFlip(port.write,bytes([probetrig]))
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
            subResp=event.getKeys(keyList=['up','left'], timeStamped=clock)
            win_count=win_count+1
            if win_count==max_win_count:
                break
        
        if not subResp:
            if EEGflag:
                port.write(subNonRespTrig)
                resp_trig=subNonRespTrig
            
            trial_corr=np.nan
            RT=np.nan
            key='None'
        else:
            if EEGflag:
                port.write(subRespTrig)
                resp_trig=subRespTrig
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
        for shape in other_stim:
            shape.autoDraw=False
        for bar in bars:
            bar.autoDraw=False
        target_stim.autoDraw=False
        distractor_stim.autoDraw=False
        
        win.flip()
        #core.wait(ITI)
        
        for stim in stimuli:
            if (stim.pos[0]==which_circle.pos[0]) and (stim.pos[1]==which_circle.pos[1]):
                target_circle=stim
        if (thisBlock[trial]=='neut' and disAorP=='P') or (thisBlock[trial]=='dis'): #if there is no distractor this trial we want to document that
            for stim in stimuli:
                if (stim.pos[0]==distractor_stim_clock[0]) and (stim.pos[1]==distractor_stim_clock[1]):
                    distractor_circle=stim
            stim_loc=(target_circle.name,distractor_circle.name)
            dis_name=distractor_stim.name
        else:
            stim_loc=(target_circle.name,'noDis')
            dis_name='noDis'
        
        # # translating things so that the output to the CSV file is a bit more readable
        if thisBlock[trial]=='neut':
            if disAorP=='A':
                neutCue_type='Absent'
            else:
                neutCue_type='Present'
        else:  
            neutCue_type='Present'
        
        if EEGflag:
            Thistrial_data= {'trialNum':(trial),'trial_type':thisBlock[trial],'dis_type':neutCue_type,'corrResp':corrKey,'subjectResp':key,'trialCorr?':trial_corr,'RT':RT,
                            'Tar,Dis,Other':(target_stim.name,dis_name,other_stim[0].name), 'stim_loc':stim_loc,'ITI':ITI,'trial_trigs':(thistrialFlag,probetrig,resp_trig)}
        else:
            Thistrial_data= {'trialNum':(trial),'trial_type':thisBlock[trial],'dis_type':neutCue_type,'corrResp':corrKey,'subjectResp':key,'trialCorr?':trial_corr,'RT':RT, 
                            'Tar,Dis,Other':(target_stim.name,dis_name,other_stim[0].name),'stim_loc':stim_loc,'ITI':ITI,'trial_trigs':'None'}
        trialDataList.append(Thistrial_data)
        
        print(Thistrial_data)
        
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
    
    blocks.update({'blockInfo_%i'%(block):{'block':block,'trialsData':trialDataList}})
    
    # #########################saving data out###########################################
    if block==0:
        make_csv(filename,expStart=True)
    else:
        make_csv(filename,expStart=False)
    if EEGflag:
        port.write(endofBlocktrig)
    if block==int(len(stimList_blocks)/2)-1:
        exit_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='You are halfway through the study!')
        exit_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Please take a break and, when done, call the experimenter over to continue')
        exit_msg.draw() 
        exit_msg3.draw()
        win.flip()
        event.waitKeys(keyList=['q'])

if EEGflag:
    port.write(stopSaveflag)
    port.close()

for stim in stimuli:
    stim.autoDraw=False
fixation.autoDraw=False
 
exit_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Thank you for participating in our experiment!')
exit_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='Your time and cooperation is greatly appreciated.')
exit_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Press any key to exit')
exit_msg.draw()
exit_msg2.draw() 
exit_msg3.draw()

win.flip()
event.waitKeys()