## Singleton search paradigm, collaboration w Shaun Vecera & Brad Stilwell
# 06/26/2020: adjusting sizing
# 04/17/2020: for EEG, we want to run our "sledgehammer" version, where we're maximizing exposure to cue as well as singleton trials, and we have placeholders.
    # ADDING target condition for EEG too. Target to be run separately
# 02/19/2020: after 02/19 meeting with shaun and brad, adding a version of the task where we have no placeholders, 
    # just a different distribution of trials-- more exposure to cue. 64 trials total, used to split neut 48 to dis 16, now its more even at 40/24.
    # Of the 40 neutrals, 32 are DisA and 8 are DisP
# 11/04/19:  Bring spatial cues closer, fix practice to match Brad's, added his instruction slides,
    # add two more shapes (adjusted circle positioning, no longer aligns with clock positions)
# 10/16/19:Changing so that background, eccentricity, and RGB values match Brad's.
# 07/17/19 REVISIONS based on meeting w Shaun and Brad yesterday: keep distractor color constant, still vary the shapes trial-by-trial
# 07/16/19 changed orientd bars to photoshopped version instead of text stim
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

expInfo = {'subject': '', 'session [t or d]':'','run':'','refresh':60,'spat_lout [all or lower]':'all','colorCode [1-5]':''}
expName='alpha_singleton_ColorConstant_MATCHING_BRAD_extraDisCues_forEEG'
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
win = visual.Window([1280,720],units='deg',fullscr=True,monitor='testMonitor',checkTiming=True,colorSpace='rgb255',color=[0,0,0]) #[1680,1050] #[1280,720]

# the vis_deg_cue and the multiplier should multiply to equal 4.66
vis_deg_multiplier=5.17777778#6.65714286#3.98290598
vis_deg_cue=.9#.7#1.17
no_stim=6

for key in ['escape']:
    event.globalKeys.add(key, func=core.quit)
    

## spat_lout: spatial layout, determines whether stimuli are only displayed in the lower half of the screen or if all locations around the circle are displayed

if expInfo['spat_lout [all or lower]'] =='all':
    pos_stim=='all'
elif expInfo['spat_lout [all or lower]'] == 'lower':
    pos_stim=='lower'
else:
    print('Please enter a valid response to the spat_lout box')
    core.quit()

## t= target, d= distractor, this is the shape that the spatial cue is pointing to for this whole run! 

if expInfo['session [t or d]']=='t':
    cue_type='tar'
elif expInfo['session [t or d]']=='d':
    cue_type='dis'
else:
    print('Please enter a valid response to the SESSION box')
    core.quit()

if expInfo['colorCode [1-5]'] not in ['1','2','3','4','5']:
    print("Please enter a valid response to the ColorCode box")
    core.quit()

## Activate the EEG triggers, set EEGflag to zero for debugging 

EEGflag=1
if EEGflag:
    port=serial.Serial('COM4',baudrate=115200)
    port.close()
    startSaveflag=bytes([254])
    stopSaveflag=bytes([255])
    #cue_onset_trig=bytes([101])
    
    cue_possibilities=['neut','dis','tar']
    
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
    
    dis_possibilities=['neutA','neutP','disP','tarP']
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
    response_trigDict={'subNonRespTrig':subNonRespTrig,'subRespTrig':subRespTrig}
    print(cue_trigDict)
    print(probe_trigDict)
    print(other_trigDict)
    print(response_trigDict)

if EEGflag:
    filename='Z:/AlphaStudy_Data/eegData/eeg_behavior_data'+u'/%s_%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session [t or d]'],expInfo['block'],expInfo['date'])
else:
    filename='Z:/AlphaStudy_Data/behavData'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session [t or d]'],expInfo['block'],expInfo['date']) #for dells
    #filename='/Volumes/rdss_kahwang/AlphaStudy_Data/behavData'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])

thisRunNum=expInfo['run']
refresh_rate=expInfo['refresh']

num_blocks=1 # blocks per run of the script

# the practice is set up to run distractor cue trials, but as of right now only shows neutral trials
def pracCond(n_practrials=8,demo=False):
    pracDataList=[]
    pracBlock=[]
    for r in range(int(n_practrials)):
        #pracBlock.append('dis')
        pracBlock.append('neut')
    for trial in range(n_practrials):
        ITI=2.0
        distractor_stim,target_stim,other_stim,other_name=generate_target()
        if trial==0:
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
        for circs in  stimuli:
            print(circs.size)
            circs.autoDraw=False
        
        if pracBlock[trial]=='neut':
            cue_circ=list(np.random.choice(stimuli,no_stim,replace=False))
            for c in cue_circ:
                #c.setLineColor([255,255,255])
                c.autoDraw=True
        elif pracBlock[trial]==cue_type:
            cue_circ=np.random.choice(stimuli,1)
            cue_circ[0].autoDraw=True
            #cue_circ[0].setLineColor([255,255,255])
            
        fixation.autoDraw=True
        
        if EEGflag:
            thistrialFlag=cue_trigDict[thisBlock[trial]+'_trig']
            win.callOnFlip(port.write,bytes([thistrialFlag]))
        
        wait_here(.9) # ############## Cue presentation ###################
        
        fixation.autoDraw=True
        for circs in stimuli:
            circs.autoDraw=False
        
        wait_here(1) # ############ delay one/SOA period ###############
        
        if pracBlock[trial]=='dis':
            cue_loc=list(stimuli).index(cue_circ[0]) #index of the distractor cue circle
            stim_minus_cue=np.delete(stimuli, cue_loc) #get a list of circles that don't include the distractor cue circ
            which_circle=np.random.choice(stim_minus_cue,1)[0] # choose the target loc
            distractor_stim_clock=(cue_circ[0].pos[0]*vis_deg_multiplier,cue_circ[0].pos[1]*vis_deg_multiplier)
            distractor_stim.pos=(distractor_stim_clock[0],distractor_stim_clock[1])#(distractor_stim_clock[0]/6,distractor_stim_clock[1]/6)
            distractor_stim.autoDraw=True
            disAorP='P'
        elif pracBlock[trial]=='neut': 
            which_circle=np.random.choice(stimuli,1)[0]
            disAorP='A'
            if disAorP=='P':
                tar_loc=list(stimuli).index(which_circle)
                stim_minus_tar=np.delete(stimuli,tar_loc)
                distractor_stim_clock=np.random.choice(stim_minus_tar,1)[0].pos
                distractor_stim_clock=(distractor_stim_clock[0]*vis_deg_multiplier,distractor_stim_clock[1]*vis_deg_multiplier)
                distractor_stim.pos=(distractor_stim_clock[0],distractor_stim_clock[1])#(distractor_stim_clock[0]/6,distractor_stim_clock[1]/6)
                distractor_stim.autoDraw=True
        
        target_stim.pos=(which_circle.pos[0]*vis_deg_multiplier,which_circle.pos[1]*vis_deg_multiplier)#(which_circle.pos[0]/6,which_circle.pos[1]/6)
        target_stim.autoDraw=True
        
        #distractor_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the distractor
        for s in range(len(stimuli)):
            circs=stimuli[s]
            bars[s].pos=other_stim[s].pos #except target and distractor
            bars[s].ori=(np.random.choice([0,90],1))[0]
            bars[s].autoDraw=True
            if not ((circs.pos[0]==which_circle.pos[0]) and (circs.pos[1]==which_circle.pos[1])):  # if this position isn't the target
                if ((pracBlock[trial]=='neut' and disAorP=='P') or pracBlock[trial]=='dis'): #if this trial has a distractor 
                    if not ((circs.pos[0]==(distractor_stim_clock[0]/vis_deg_multiplier)) and (circs.pos[1]==(distractor_stim_clock[1]/vis_deg_multiplier))): # and if this position is also not the distractor
                        #if the circle is not a target or distractor then put other_stim in it
                        other_stim[s].autoDraw=True
                else:
                    other_stim[s].autoDraw=True
            elif ((circs.pos[0]==which_circle.pos[0]) and (circs.pos[1]==which_circle.pos[1])): # if it is the target position
                target_ori=bars[s].ori #then document the orientation of the bar at this loc
                print(target_ori)
        
        if target_ori==0:
            corrKey='q'#'up'
        elif target_ori==90:
            corrKey='p'#'left'
        
        #wait_here(2) # ############### probe presentation ####################
        
        event.clearEvents()
        max_win_count=int(2/(1/refresh_rate))
        win_count=0
        subResp=None
        clock=core.Clock()
        while not subResp:
            win.flip()
            subResp=event.getKeys(keyList=['q','p'], timeStamped=clock)#['up','left']
            win_count=win_count+1
            if win_count==max_win_count:
                break
        
        if not subResp:

            trial_corr=0

        else:

            if subResp[0][0]==corrKey:
                trial_corr=1
            else:
                trial_corr=0
        pracDataList.append(trial_corr)
        fixation.draw()
        for circs in stimuli:
            circs.autoDraw=False
            #circs.lineColorSpace='rgb255'
            #circs.setLineColor([0,0,0])
            #circs.setFillColor([0,0,0])
        for shape in other_stim:
            shape.autoDraw=False
        for bar in bars:
            bar.autoDraw=False
        target_stim.autoDraw=False
        distractor_stim.autoDraw=False
        
        win.flip()
        #core.wait(ITI)
        
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
        #fieldnames=['block','trialNum','trial_type','dis_PresentorAbsent','corrResp','subResp','trialCorr?','RT','stim_loc(T,D)','ITI','Tar,Dis,Other','trial_trigs','triggers']
        
        FirstBlock=blocks['0'] #blocks is a dictionary of the block data, ie { 0 : [{trial:1,RT:1,etc },{trial:2,RT:2,etc},... ] }
        FirstTrial=FirstBlock[0]
        fieldnames=list(FirstTrial.keys()) + ['block','triggers','run','colorCode']
        #fieldnames is simply asserting the categories at the top of the CSV
        writer=csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writeheader()
        print('\n\n\n')
        for n in range(len(blocks.keys())): # loop through each block
            ThisTrialList=blocks[str(n)] #grabbing the block info for this block
            #print(ThisBlock)
            #print('\n')
            for k in range(len(ThisTrialList)): #this should be the # of trials
                ThisTrial=ThisTrialList[k] #grabbing the trial info out of data for this trial
                #print(ThisTrial)
                
                #combining all the dictionaries into one to write to row
                dataDict= ThisTrial.copy()
                dataDict.update({'block':str(n)})
                dataDict.update({'run':ThisRunNum,'colorCode':expInfo['colorCode [1-5]']})
                if EEGflag and expStart==True and k==0:
                     dataDict.update({'triggers':(cue_trigDict,probe_trigDict,response_trigDict,other_trigDict)})
                else:
                    dataDict.update({'triggers':''})
                
                writer.writerow(dataDict)

if pos_stim=='all':
#    noon_oclock = visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',
#    
#        win=win, name='12',
#        
#        size=(0.47,1.17), units='deg', 
#
#        ori=0, pos=(0, vis_deg_cue), opacity=1, depth=-1.0, interpolate=True)
#
#    noon_oclock.setAutoDraw(True)
    one_oclock = visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',
    
            win=win, name='1',
    
            size=(0.47,1.17), units='deg', #pos=(1.17,1.17),
    
            ori=45, pos=(vis_deg_cue*(sqrt(2)/2), ((sqrt(2)/2)*vis_deg_cue)),
            opacity=1, depth=-1.0, interpolate=True)
    
    one_oclock.setAutoDraw(True)
    three_oclock = visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',
        win=win, name='3',

        size=(0.09, 0.15),

        ori=90, units='deg', 

           pos=(vis_deg_cue, 0),

        opacity=1, depth=-3.0, interpolate=True)

    three_oclock.setAutoDraw(True)
    
    five_oclock = visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',

        win=win, name='5',

        size=(0.09, 0.15),

        ori=135, pos=(vis_deg_cue*(sqrt(2)/2), -((sqrt(2)/2)*vis_deg_cue)),

        opacity=1, depth=-5.0, interpolate=True)

    five_oclock.setAutoDraw(True)
#    six_oclock = visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',
#    
#        win=win, name='6',
#        
#        size=(0.47,1.17), units='deg', 
#
#        ori=0, pos=(0, -vis_deg_cue), opacity=1, depth=-1.0, interpolate=True)
#    six_oclock.setAutoDraw(True)
    seven_oclock =visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',

        win=win, name='7',

        size=(0.09, 0.15),

        ori=225, pos=(-vis_deg_cue*(sqrt(2)/2), -((sqrt(2)/2)*vis_deg_cue)),

        opacity=1, depth=-5.0, interpolate=True)

    seven_oclock.setAutoDraw(True)
    nine_oclock = visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',

        win=win, name='9',

        size=(0.09, 0.15),

        ori=90, pos=(-vis_deg_cue, 0),

        opacity=1, depth=-3.0, interpolate=True)

    nine_oclock.setAutoDraw(True)
    eleven_oclock =visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',

        win=win, name='11',

        size=(0.09, 0.15),

        ori=315, pos=(-vis_deg_cue*(sqrt(2)/2), ((sqrt(2)/2)*vis_deg_cue)),

        opacity=1, depth=-1.0, interpolate=True)
    eleven_oclock.setAutoDraw(True)
    stimuli=[one_oclock,three_oclock,five_oclock,seven_oclock,nine_oclock,eleven_oclock]
    right_stim=stimuli[:3]
    left_stim=stimuli[3:]
elif pos_stim=='lower': # the 'lower' flag makes it so that all stimuli are presented in the lower half of the screen (not acutal clock positions anymore)

    four_oclock = visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',
        win=win, name='4',

        size=(0.09, 0.15),

        ori=90, units='deg', 

           pos=(((sqrt(2)/2)*vis_deg_cue), (-1*vis_deg_cue*(sqrt(2)/2))),

        opacity=1, depth=-3.0, interpolate=True)

    four_oclock.setAutoDraw(True)
    three_oclock = visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',
        win=win, name='3',

        size=(0.09, 0.15),

        ori=90, units='deg', 

           pos=(((sqrt(3)/2)*vis_deg_cue), (-1*vis_deg_cue*(1/2))),

        opacity=1, depth=-3.0, interpolate=True)

    three_oclock.setAutoDraw(True)
    five_oclock = visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',

        win=win, name='5',

        size=(0.09, 0.15),

        ori=135, pos=(vis_deg_cue*(1/2), -((sqrt(3)/2)*vis_deg_cue)),

        opacity=1, depth=-5.0, interpolate=True)

    five_oclock.setAutoDraw(True)



    seven_oclock =visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',

        win=win, name='7',

        size=(0.09, 0.15),

        ori=225, pos=(-vis_deg_cue*(1/2), -((sqrt(3)/2)*vis_deg_cue)),

        opacity=1, depth=-5.0, interpolate=True)

    seven_oclock.setAutoDraw(True)
    eight_oclock =visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',

        win=win, name='8',

        size=(0.09, 0.15),

        ori=225, pos=((-vis_deg_cue*(sqrt(2)/2)), -((sqrt(2)/2)*vis_deg_cue)),

        opacity=1, depth=-5.0, interpolate=True)

    eight_oclock.setAutoDraw(True)
    nine_oclock = visual.ImageStim(image=os.getcwd()+'/stimuli/grey_Verticle.png',

        win=win, name='9',

        size=(0.09, 0.15),

        ori=90, pos=((-1*vis_deg_cue*(sqrt(3)/2)), (-1*(1/2)*vis_deg_cue)),

        opacity=1, depth=-3.0, interpolate=True)

    nine_oclock.setAutoDraw(True)

    stimuli=[three_oclock,four_oclock,five_oclock,seven_oclock,eight_oclock,nine_oclock]
    right_stim=stimuli[:3]
    left_stim=stimuli[3:]



#size=94.66,3.6)
diamond_size=(4.66,3.6)
images={'blue_diamond':visual.ImageStim(win=win,name='blue_diamond', units='deg', 
    ori=0, size=diamond_size,image=os.getcwd()+'/stimuli/blue_diamond_eq.png'),
    'orange_diamond':visual.ImageStim(win=win,name='orange_diamond', units='deg', 
    ori=0, size=diamond_size,image=os.getcwd()+'/stimuli/orange_diamond.png'),
    'green_diamond':visual.ImageStim(win=win,name='green_diamond', units='deg', 
    ori=0, size=diamond_size,image=os.getcwd()+'/stimuli/green_diamond.png'),
    'pink_diamond':visual.ImageStim(win=win,name='pink_diamond', units='deg', 
    ori=0, size=diamond_size,image=os.getcwd()+'/stimuli/pink_diamond.png'),
    'red_diamond':visual.ImageStim(win=win,name='red_diamond', units='deg', 
    ori=0, size=diamond_size,image=os.getcwd()+'/stimuli/red_diamond_eq.png'),
    'yellow_diamond':visual.ImageStim(win=win,name='yellow_diamond', units='deg', 
    ori=0, size=diamond_size,image=os.getcwd()+'/stimuli/yellow_diamond_eq.png'),
    'blue_circle':visual.ImageStim(win=win,name='blue_circle', units='deg', 
    ori=0, size=circ_size,image=os.getcwd()+'/stimuli/blue_circle_eq.png'),
    'red_circle':visual.ImageStim(win=win,name='red_circle', units='deg', 
    ori=0, size=circ_size,image=os.getcwd()+'/stimuli/red_circle_eq.png'),
    'yellow_circle':visual.ImageStim(win=win,name='yellow_circle', units='deg', 
    ori=0, size=circ_size,image=os.getcwd()+'/stimuli/yellow_circle_eq.png'),
    'orange_circle':visual.ImageStim(win=win,name='orange_circle', units='deg', 
    ori=0, size=diamond_size,image=os.getcwd()+'/stimuli/orange_circle.png'),
    'pink_circle':visual.ImageStim(win=win,name='pink_circle', units='deg', 
    ori=0, size=circ_size,image=os.getcwd()+'/stimuli/pink_circle.png'),
    'green_circle':visual.ImageStim(win=win,name='green_circle', units='deg', 
    ori=0, size=circ_size,image=os.getcwd()+'/stimuli/green_circle.png'),
    'grey_diamond':visual.ImageStim(win=win,name='grey_diamond', units='deg', 
    ori=0, size=diamond_size,image=os.getcwd()+'/stimuli/grey_diamond.png'),
    'grey_circle':visual.ImageStim(win=win,name='grey_circle', units='deg', 
    ori=0, size=diamond_size,image=os.getcwd()+'/stimuli/grey_circle.png')}
images_names=list(images.keys())


colors_list=['red','blue','pink','yellow','orange']
neut_color='green'#two_colors[0] #neutral is always green now
dist_color=colors_list[int(expInfo['colorCode [1-5]'])-1] #using the color code as the index

## generate_target() gives the shapes that will become the target, distractor, and neutral shapes. can be called once per block or per trial, depending on how often you want colors to be changed out

def generate_target():
    
    potential_dis_shapes=[shape for shape in images_names if dist_color in shape]
    
    distractor_name=np.random.choice(potential_dis_shapes,1)[0]
    
    target_color=neut_color
    
    if 'circle' in distractor_name:
        target_shape='diamond'
        other_shape='circle'
    elif 'diamond' in distractor_name:
        target_shape='circle'
        other_shape='diamond'
    
    distractor_stim=images[distractor_name]
    target_stim=images[target_color+'_'+target_shape]
    other_name=target_color+'_'+other_shape
    other_stim=[visual.ImageStim(win=win,image=images[other_name].image, units='deg',ori=0,size=images[other_name].size,name=other_name) for i in range(no_stim)] # making 4 copies of Other_shape 
    for g in range(no_stim):
        #other_stim[g].autoDraw=True
        other_stim[g].pos=(stimuli[g].pos[0]*vis_deg_multiplier,stimuli[g].pos[1]*vis_deg_multiplier)#(stimuli[g].pos[0]/6,stimuli[g].pos[1]/6)#
        #print(stimuli[g].pos)
    
    print(target_stim.name)
    print(distractor_stim.name)
    print(other_stim[0].name)
    
    for stim in stimuli:
        #stim.size=(1.5,1.5)
        stim.size=(0.47,1.17)
        stim.lineWidth=0.47#5
        stim.pos=(stim.pos[0],stim.pos[1])
    
    distractor_stim.opacity=1
    target_stim.opacity=1
    #distractor_stim.autoDraw=True
    #target_stim.autoDraw=True
    return distractor_stim,target_stim,other_stim,other_name

fixation = visual.TextStim(win, text='+',pos=(0,0.005),units='norm', color=(1,1,1))
fixation.size=0.6

#disc_bar=visual.ImageStim(win=win,name='bar', units='deg', 
 #   ori=0,size=disc_bar_size,image=os.getcwd()+'/stimuli/Verticle.png') #visual.TextStim(win, text='|',units='deg', color=(1,1,1))
disc_bar_size=(1.4,1.63)#
bars=[visual.ImageStim(win=win,name='bar', units='deg', ori=0,size=disc_bar_size,image=os.getcwd()+'/stimuli/grey_Verticle.png')  for i in range(no_stim)]
placeholdersDia=[visual.ImageStim(win=win,name=('GreyDia%i'%(i)), units='deg', ori=0,size=size,image=images['grey_diamond'].image,
                    pos=(stimuli[i].pos[0]*vis_deg_multiplier,stimuli[i].pos[1]*vis_deg_multiplier))  for i in range(no_stim)]

for circs in stimuli:
    circs.autoDraw=False

## Display task instruction screens

intro_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Welcome to the experiment!')
intro_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='You will see a series circles, then a series of shapes. You must find the shape that is unique. This is the target shape.')#You must find the target shape. The target shape is the %s' % (target_stim.name.split('_')[0])+' '+(target_stim.name.split('_')[1]))
intro_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Press any key to continue')
intro_msg.draw()
intro_msg2.draw() 
intro_msg3.draw()
win.flip()
event.waitKeys()
intro_mesg4= visual.TextStim(win,pos=[0,.6],units='norm',text='Please remain focused on the cross in the middle of the screen whenever there are NOT circles on the screen.')
intro_mesg5=visual.TextStim(win,pos=[0,0], units='norm',text='Respond to the orientation of the line in the target shape using the Q and P keys on the keyboard')
intro_mesg6=visual.TextStim(win,pos=[0,-0.6],units='norm',text='You will also sometimes see a pop-out color. The cue lines help you find the unique shape, while ignoring the pop-out color. Press any key to continue.')
intro_mesg4.draw()
intro_mesg5.draw()
intro_mesg6.draw()
win.flip()
event.waitKeys()
instruction_slide1=visual.ImageStim(win=win,image=os.getcwd()+'/instruction_slides/Slide1.JPG')
instruction_slide1.draw()
win.flip()
event.waitKeys()
if cue_type =='dis':
    instruction_slide2=visual.ImageStim(win=win,image=os.getcwd()+'/instruction_slides/distractorCueInst.JPG')
    instruction_slide2.draw()
elif cue_type =='tar':
    instruction_slide2=visual.ImageStim(win=win,image=os.getcwd()+'/instruction_slides/targetCueInst.png')
    instruction_slide2.draw()
win.flip()
event.waitKeys()



stimList=[] #list of trials
cuePosList=[]
# 64 trials in ea block 
# 5/8 of all trials should be neutral, 3/8 spatial cues (distractor or target)
for n in range(40):#(48): #hard coding the # of trials to match brad
    stimList.append('neut')
for n in range(24): #16
    stimList.append(cue_type)
for n in range(24/no_stim): #hopefully this divides evenly (it does if only 6 circles)
    for no_positions in range(no_stim):
        cuePosList.append(no_position) # will append one of each circle position ea time it loops, to control for the number of times any one circle position is cued

stimList_blocks=[] #list of blocks, which contains a list of trials
for n in range(num_blocks): 
    stimList_scramble=list(np.random.permutation(stimList))
    stimList_blocks.append(stimList_scramble)

if EEGflag:
    port.open()
    #win.callonFlip(pport.setData,delay1trig)
    port.write(startSaveflag)
    #port.close()

likely_dis= np.random.choice(stimuli,1)[0]

blocks={}

## if this is the first time we're intializing the script, run through the practice 

if thisRunNum==1:
    pracCond(n_practrials=20,demo=False)

## Enter block loop

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
    
    neutCue=[] # of the neutral blocks, 32 are DisA and 8 are DisP
    for r in range(8):
        neutCue.append('P')
    for r in range(32):
        neutCue.append('A')
    # we assign these to each neutral trial by calling this list and popping off the P's or A's until the end of the loop
    
    print(thisBlock)
    neutCue_scramble=list(np.random.permutation(neutCue))
    cuePosList_scramble=list(np.random.permutation(cuePosList)) # this is a scrambled list of clock positions to cue to, the len of the number of cue_type trials 
    #print(disCue_scramble)
    
    ## Enter trial loop
    
    for trial in range(len(thisBlock)):
        distractor_stim,target_stim,other_stim,other_name=generate_target()
        ITI=make_ITI()
        
        print(thisBlock[trial])
        for circs in  stimuli:
            print(circs.size)
            circs.autoDraw=False
        for p in placeholdersDia:
            p.autoDraw=False
        
        if thisBlock[trial]=='neut': # if this is a neutral trial, then we draw all the cues and all the placeholders 
            for c in range(len(stimuli)):
                stimuli[c].autoDraw=True
                #placeholdersCircs[c].autoDraw=True
                placeholdersDia[c].autoDraw=True
        elif thisBlock[trial]==cue_type: # otherwise, we pick a place to cue randomly, and we point the cue there and place a placeholder there too
            cue_loc=cuePosList_scramble.pop()#np.random.choice(no_stim,1)[0]
            cue_circ=stimuli[cue_loc]
            cue_circ.autoDraw=True
            placeholdersDia[cue_loc].autoDraw=True
            
        fixation.autoDraw=True
        
        if EEGflag:
            thistrialFlag=cue_trigDict[thisBlock[trial]+'_trig']
            win.callOnFlip(port.write,bytes([thistrialFlag]))
        
        wait_here(.9) # ############## Cue presentation ###################
        
        fixation.autoDraw=True
        for circs in stimuli:
            circs.autoDraw=False
        for placeholder in placeholdersDia:
            placeholder.autoDraw=False
        
        wait_here(1) # ############ delay one/SOA period ###############
        
        if thisBlock[trial]=='dis':
            #cue_loc=list(stimuli).index(cue_circ[0]) #index of the distractor cue circle
            stim_minus_cue=np.delete(stimuli, cue_loc) #get a list of circles that don't include the distractor cue circ
            which_circle=np.random.choice(stim_minus_cue,1)[0] # choose the target loc randomly, as long as it's not the distractor 
            distractor_stim_clock=(cue_circ.pos[0]*vis_deg_multiplier,cue_circ.pos[1]*vis_deg_multiplier)
            distractor_stim.pos=(distractor_stim_clock[0],distractor_stim_clock[1])#(distractor_stim_clock[0]/6,distractor_stim_clock[1]/6)
            distractor_stim.autoDraw=True
            target_stim.pos=(which_circle.pos[0]*vis_deg_multiplier,which_circle.pos[1]*vis_deg_multiplier)
            target_stim.autoDraw=True
            disAorP='P'
        elif thisBlock[trial]=='tar':
            #cue_loc=list(stimuli).index(cue_circ[0]) #index of the tar cue circle
            stim_minus_cue=np.delete(stimuli, cue_loc) #get a list of circles that don't include the target cue circ
            which_circle=cue_circ # which_circle is always assigned as the target, since this is target cue condition we already know where which_circle is located
            target_stim_clock=(which_circle.pos[0]*vis_deg_multiplier,which_circle.pos[1]*vis_deg_multiplier)
            target_stim.pos=(target_stim_clock[0],target_stim_clock[1])
            target_stim.autoDraw=True
            distractor_stim_clock=np.random.choice(stim_minus_cue,1)[0].pos
            distractor_stim_clock=(distractor_stim_clock[0]*vis_deg_multiplier,distractor_stim_clock[1]*vis_deg_multiplier)
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
                distractor_stim_clock=(distractor_stim_clock[0]*vis_deg_multiplier,distractor_stim_clock[1]*vis_deg_multiplier)
                distractor_stim.pos=(distractor_stim_clock[0],distractor_stim_clock[1])#(distractor_stim_clock[0]/6,distractor_stim_clock[1]/6)
                distractor_stim.autoDraw=True
            target_stim.pos=(which_circle.pos[0]*vis_deg_multiplier,which_circle.pos[1]*vis_deg_multiplier)
            target_stim.autoDraw=True
        
        #distractor_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the distractor
        for s in range(len(stimuli)):
            circs=stimuli[s]
            bars[s].pos=other_stim[s].pos #except target and distractor
            bars[s].ori=(np.random.choice([0,90],1))[0]
            bars[s].autoDraw=True
            if not ((circs.pos[0]==which_circle.pos[0]) and (circs.pos[1]==which_circle.pos[1])):  # if this position isn't the target
                if ((thisBlock[trial]=='neut' and disAorP=='P') or thisBlock[trial]==cue_type): #if this trial has a distractor 
                    if not ((circs.pos[0]==(distractor_stim_clock[0]/vis_deg_multiplier)) and (circs.pos[1]==(distractor_stim_clock[1]/vis_deg_multiplier))): # and if this position is also not the distractor
                        #if the circle is not a target or distractor then put other_stim in it
                        other_stim[s].autoDraw=True
                else:
                    other_stim[s].autoDraw=True
            elif ((circs.pos[0]==which_circle.pos[0]) and (circs.pos[1]==which_circle.pos[1])): # if it is the target position
                target_ori=bars[s].ori #then document the orientation of the bar at this loc
                print(target_ori)
        
        if target_ori==0:
            corrKey='q'#'up'
        elif target_ori==90:
            corrKey='p'#'left'
        
        if EEGflag:
                # port.flush()
                probetrig=probe_trigDict[thisBlock[trial]+disAorP+'_trig']
                win.callOnFlip(port.write,bytes([probetrig]))
        
        #wait_here(2) # ############### probe presentation ####################
        
        event.clearEvents()
        max_win_count=int(2/(1/refresh_rate))
        win_count=0
        subResp=None
        clock=core.Clock()
        while not subResp:
            win.flip()
            subResp=event.getKeys(keyList=['q','p'], timeStamped=clock)#['up','left']
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
            circs.autoDraw=False
            #circs.lineColorSpace='rgb255'
            #circs.setLineColor([0,0,0])
            #circs.setFillColor([0,0,0])
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
        if (thisBlock[trial]=='neut' and disAorP=='P') or (thisBlock[trial]==cue_type): #if there is no distractor this trial we want to document that
            for stim in stimuli:
                if (stim.pos[0]==(distractor_stim_clock[0]/vis_deg_multiplier)) and (stim.pos[1]==(distractor_stim_clock[1]/vis_deg_multiplier)):
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
    
    blocks.update({str(block):trialDataList})
    
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
        event.waitKeys(keyList=['z'])

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