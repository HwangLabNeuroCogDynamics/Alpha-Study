# ##############test##################

# Hwang Lab alpha study #

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


#testing github

# Ensure that relative paths start from the same directory as this script

_thisDir = os.path.dirname(os.path.abspath(__file__))

os.chdir(_thisDir)

# Store info about the experiment session

expName = 'alpha_pilot'  # from the Builder filename that created this script

expInfo = {'subject': '', 'session': '01','f or b?':'f','no stim':'10','t in d?':'n', 'lat?':'n','COMPUTER (b,e,d,m)':'b'}

# where 'f or b?' is flexible v blocked. blocked is default

#'no stim' refers to number of potential cued locations (12 by default)

#'d in t?' refers to having trials where distractor appears in a target cued location some portion of the time (resp should be y or n) 

# lat?' lateralized stim. default is non lat stim. resp should be y or n.. THIS FLAG IS NOT YET CODED

# COMPUTER is the flag for which computer you're using, because this will influence the path to the I and T stimuli. Default is the behavioral computer. b=behavioral Dell, e=EEG dell, d=Dillan's laptop, m=Mac in Dillan's office  

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

if dlg.OK == False:

    core.quit()  # user pressed cancel

expInfo['date'] = data.getDateStr()  # add a simple timestamp

expInfo['expName'] = expName

from psychopy import visual, core

win = visual.Window([1680,1050],units='deg',fullscr=True,monitor='testMonitor')

# ###############Flags####################################################################################



# this is where we'll flag the different piloted conditions



#will blocks be flexbile or predictable?

if expInfo['f or b?']=='f':

    flex_cond_flag = True

else:

    flex_cond_flag = False



#number of cue locations

no_stim = float(expInfo['no stim'])



# target in the distractor location condition?

if expInfo['t in d?']=='y':

    TarindistFlag=True

else:

    TarindistFlag=False



#lateralized stim presentation? This doesn't do anything right now--it's all bilateral

if expInfo['lat?']=='y':

    lat_stim_flag=True

else:

    lat_stim_flag=False


# # MAKE SURE PATH TO STIMULI IS THE RIGHT ONE FOR THE COMPUTER YOU'RE USING


if expInfo['COMPUTER (b,e,d,m)']=='b': 
    target_stim=visual.ImageStim(win, image='C:\Stimuli\T2.png') 
    distractor_stim=visual.ImageStim(win, image='C:\Stimuli\I3.png') #behavioral stimulus presentation Dell
    filename='Z:/AlphaStudy/behavData'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])
    refresh_rate=50
elif expInfo['COMPUTER (b,e,d,m)']=='d':
    target_stim=visual.ImageStim(win, image='C:\\Users\\dillc\\Downloads\\T2.png')
    distractor_stim=visual.ImageStim(win, image='C:\\Users\\dillc\\Downloads\\I3.png') #dillan's computer
    filename='C:/Users/dillc/Documents'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])
    refresh_rate=50
elif expInfo['COMPUTER (b,e,d,m)']=='m':
    target_stim=visual.ImageStim(win, image='/Users/dcellier/Documents/GitHub/Alpha-Study/stimuli/T2.png') 
    distractor_stim=visual.ImageStim(win, image='/Users/dcellier/Documents/GitHub/Alpha-Study/stimuli/I3.png')
    filename='/Users/Shared/'+u'data/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])
elif expInfo['COMPUTER (b,e,d,m)']=='e':
    target_stim=visual.ImageStim(win, image='C:\Stimuli\T2.png') 
    distractor_stim=visual.ImageStim(win, image='C:\Stimuli\I3.png') #EEG stimulus presentation Dell
    filename='Z:/AlphaStudy/eegData'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])
    refresh_rate=50
else:
    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    filename = _thisDir + os.sep + u'data/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])

cue_types=['target','distractor'] # distractor or target or neutral cues

cue_valid=[.5,.8] # cue validity

num_trials=33 # change later to 33

num_reps=3 #the number of repeats for each condition, should be 3 in experiment

stimList=[]

for cue in cue_types:

    for num in cue_valid:

        stimList.append({'cue':cue,'validity':num})

stimList.append({'cue':'neutral','validity':0})

print(stimList)

cue_type_reps=len(cue_valid)*num_reps #the number of times that the 'target' or 'distractor' cue types should be repeated is equal to the number of validity types (i.e. 2 per cue type) times the n repeats for each condition (ie, 3)

EEGflag=0
if expInfo['COMPUTER (b,e,d,m)']=='e':
    EEGflag=1
    #added trigs
    startSaveflag=bytes([254])
    stopSaveflag=bytes([255])
    delay1trig=bytes([101])
    probetrig=bytes([103])
    ITItrig=bytes([115])
    tIdtrig=bytes([117])
    target5trig=bytes([105])
    target8trig=bytes([107])
    dis5trig=bytes([109])
    dis8trig=bytes([111])
    neutraltrig=bytes([113])
    
    port=serial.Serial('COM4',baudrate=115200) # based on the biosemi website-- may be wrong?

# ####stimulus##############################################################################################

def wait_here(t):
    interval=1/refresh_rate
    num_frames=int(t/interval)
    for n in range(num_frames):
        draw_fixation()
        win.flip()

def draw_fixation(): #0 to 1, for the opacity

    fixation.draw()


def pracCond(thisBlock,n_practrials=10):
    pracDataList=[]
    for n in range(n_practrials):
    
        ITI=make_ITI('b')

        # info for this block --for subject ######################################

        if n==0:

            for circs in stimuli:

                circs.opacity = 0 

            info_msg3=visual.TextStim(win,pos=[0,0],units='norm',text='Begin practice block')

            info_msg3.draw()

            win.update()
            core.wait(2)

            draw_fixation()

            win.flip()

            core.wait(3)# pre-block pause

        

        for circs in stimuli:

            circs.opacity=1

            circs.setLineColor([0,0,0])

            circs.setFillColor([0,0,0])

        

        if not flex_cond_flag: # if the block is BLOCKED

            if n==0: #and its the first trial

                # randomly select two circles to cue

                cue_target_1=np.random.choice(right_stim,1)

                cue_target_2=np.random.choice(left_stim,1)

        else: #otherwise, select a new circle every time

            cue_target_1=np.random.choice(right_stim,1)

            cue_target_2=np.random.choice(left_stim,1)



        #ensure that cue'd circles don't end up too close to each other, ie at clock positions 12 and 1, or 6 and 7
        if no_stim==12:
            while ((cue_target_1[0] is noon)and(cue_target_2[0] is one_oclock)) or ((cue_target_1[0] is six_oclock) and (cue_target_2[0] is seven_oclock)):
    
                cue_target_1=np.random.choice(stimuli[:6],1)
    
                cue_target_2=np.random.choice(stimuli[6:],1)


        color_ind=cue_types_scramble.index(thisBlock['cue'])
        cue_target_1[0].setLineColor(colors_scramble[color_ind])
        cue_target_2[0].setLineColor(colors_scramble[color_ind])
    

        draw_fixation()

        win.flip()

        core.wait(.5) # CUE PERIOD #################################################

        

        draw_fixation()

        # ## SOA period

        for circs in stimuli:

            circs.setLineColor([0,0,0])

        

        win.flip()

        core.wait(1.5) # DELAY #####################################################

        

        draw_fixation()

        

        target_loc1 = list(right_stim).index(cue_target_1[0]) #where are the two cued circles?

        stim_minus_one = np.delete(right_stim, target_loc1) 

        target_loc2 = list(left_stim).index(cue_target_2[0]) 

        stim_minus_two = np.delete(left_stim,target_loc2) #get a list of stimuli that don't include cued circles

        

        

        if thisBlock['validity']==.5: # THIS GIVES HALF THE CHANCE TO EITHER CUED SPOT, SO ANY ONE CUED SPOT HAS .25 or .40 chance of selection

            which_circle= np.random.choice([cue_target_1[0], cue_target_2[0], stim_minus_two],1,p=[0.25,0.25,0.5]) #decide if cue is valid, using validity % of this condition

        elif thisBlock['validity']==.8:

            which_circle= np.random.choice([cue_target_1[0], cue_target_2[0], stim_minus_two],1,p=[0.4,0.4,0.2])



        

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

                    distractor_stim.pos=(np.random.choice(right_stim,1))[0].pos

                else:

                    distractor_stim.pos= (np.random.choice(left_stim,1))[0].pos

            

            else: #if this trial is invalid 

                    tar=np.random.choice(stim_minus_one,1,replace=False) #select two circles that aren't the cued circles

                    dist=np.random.choice(stim_minus_two,1,replace=False)

                    distractor_stim.pos=dist[0].pos #put the distractor in one and the target in the other

                    target_stim.pos=tar[0].pos

    

        elif thisBlock['cue']=='distractor':

            

            if trial_type=='valid': #if this trial's cued locations are valid, put the distractor in one of them

                distractor_stim.pos=which_circle[0].pos

                if cue_side=='L': #if the dist is on the Left side of the clock, we want the target on the right and vice versa

                    target_stim.pos=(np.random.choice(right_stim,1))[0].pos

                else:

                    target_stim.pos= (np.random.choice(left_stim,1))[0].pos

            

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

        distractor_stim.draw()

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

        

        for circs in stimuli: 

            if not (((circs.pos[0]==target_stim.pos[0]) and (circs.pos[1]==target_stim.pos[1])) or ((circs.pos[0]==distractor_stim.pos[0]) and (circs.pos[1]==distractor_stim.pos[1]))): #if the circle isn't a target or distractor, its grey

                circs.setLineColor([0,0,0])

                circs.setFillColor(None)

            else:

                circs.setLineColor([1,-1,-1])

                circs.setFillColor(None)

        

        win.update()

        

        clock=core.Clock()

        subResp= event.waitKeys(1.5,keyList=['up','down','left','right'],timeStamped=clock)

        if subResp==None:

            trial_corr=-1

            RT=-1

            key="None"

        else:

            if subResp[0][0]==corrKey:

                trial_corr=1

            else:

                trial_corr=0

            RT=subResp[0][1]

            key=subResp[0][0]

        

        #core.wait(0) # PROBE AND RESP ##############################################

        

        draw_fixation()

        

        for circs in stimuli:

            circs.setLineColor([0,0,0])

            circs.setFillColor([0,0,0])

        

        #this my have to be rounded up or down depending on refresh rate? see: https://discourse.psychopy.org/t/jittering-iti-by-code-in-the-builder/4116

        #ITI=round(1,ITI)

        

        Thistrial_data= trial_corr

        pracDataList.append(Thistrial_data)

        #print(trialDataList)

        win.flip()

        core.wait(ITI)
        for circs in stimuli:
            circs.opacity=0
    
    acc_feedback=visual.TextStim(win, pos=[0,0],units='norm',text='Your accuracy for the practice round was %i percent. Practice again? (y/n)' %(100*(np.sum(pracDataList)/n_practrials)))
    acc_feedback.draw()
    win.update()
    cont=event.waitKeys(keyList=['y','n'])
    if cont[0]=='y':
        pracCond(thisBlock,n_practrials)

def make_csv(filename):
    
    with open(filename+'.csv', mode='w') as csv_file:
    
        fieldnames=['flex or blocked?','no stim','TarInDistFlag','lateralized?','block','cue','validity','trialNum','trial_type','corrResp','subResp','trialCorr?','RT','stim_loc(T,D)','tarinDisCond','ITI']
    
        #fieldnames is simply asserting the categories at the top of the CSV
    
        writer=csv.DictWriter(csv_file,fieldnames=fieldnames)
    
        writer.writeheader()
    
        
    
        #writer.writerow({'flex or blocked?': flex_cond_flag,'no stim':expInfo['no stim'],'TarInDistFlag':TarindistFlag,'lateralized?':lat_stim_flag})
        #This is just to give info about the session overall: was the session blocked or flexibly cued? How many stim? etc.
    
        print('\n\n\n')
    
        for n in range(len(blocks.keys())): # loop through each block
            blocks_data = list(blocks.keys())[n]
     
            ThisBlock=blocks[blocks_data] #grabbing the block info for this block
            #print(ThisBlock)
            #print('\n')
    
            for k in range(len(ThisBlock['trialsData'])): #this should be the # of trials
                ThisTrial=ThisBlock['trialsData'][k] #grabbing the trial info out of data for this trial
                #print(ThisTrial)
                writer.writerow({'flex or blocked?': flex_cond_flag,'no stim':expInfo['no stim'],'TarInDistFlag':TarindistFlag,'lateralized?':lat_stim_flag,'block':ThisBlock['block'],'cue':ThisBlock['cueType'],'validity':ThisBlock['validity'],

                                'trialNum':ThisTrial['trialNum'],'trial_type':ThisTrial['trial_type'],

                                'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],

                                'RT':ThisTrial['RT'],'stim_loc(T,D)':ThisTrial['stim_loc'],'tarinDisCond':ThisTrial['tarinDisCond'],

                                'ITI':ThisTrial['ITI']})


def make_ITI(exp_type):
    if exp_type=='b' or exp_type=='m' or exp_type=='d':
        ITI=np.random.choice([1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6],1)[0] #averages to around 2 second?
    elif exp_type=='e':
        ITI=np.random.choice([3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6],1)[0] # averages to around 4 seconds?
    return ITI

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



#draw_fixation()

win.flip()

vis_deg=3.5

if no_stim==12:

    noon = visual.Circle(

        win=win, name='12',

        size=(0.60, 0.60),

        ori=0, pos=(0, vis_deg),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=0.0, interpolate=True)

    noon.setAutoDraw(True)

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

    six_oclock = visual.Circle(

        win=win, name= '6', 

        size=(.09,0.15),  ori=0, pos=(0, -vis_deg),

        lineWidth=7, lineColor=None, fillColor=None)

    six_oclock.setAutoDraw(True)

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

    stimuli=[one_oclock,two_oclock,three_oclock,four_oclock,five_oclock,six_oclock,seven_oclock,eight_oclock,nine_oclock,ten_oclock,eleven_oclock,noon]
    right_stim=stimuli[:6]
    left_stim=stimuli[6:]

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


# ############################################blocks######################################


#blocks=data.TrialHandler(stimList,num_reps)#,3,method='sequential') #three repeats each, randomly assorted but each cond is completed before they recycle #change to 3
blocks={}
if EEGflag:
    port.close()
    port.open()
    #win.callonFlip(pport.setData,delay1trig)
    port.write(startSaveflag)
    port.flush()
    wait_here(.2)
    port.close()
#we want to initialize another list of cues wherein the order is randomized so that target blocks or neutral or distractor blocks come first, counterbalanced over subjects
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

print(cue_types_scramble)
k=0
for cue in cue_types_scramble: #looping through the types of cues in sequence, since we care about the order now. 
    if cue=='neutral':
        reps=num_reps #if the cue type is neutral, we don't want to run it for the full # of cue_type_reps. We just want it to be run for num_reps
    else:
        reps=cue_type_reps
    
    valid_count=[]
    
    for block in (range(reps)): #we want each cue type to repeat (num_reps * the # of validity conds) times 
        
        if cue =='neutral':
            thisValid=0.0
        else:
            if (valid_count.count(0.5)<(num_reps)) and (valid_count.count(0.8)<(num_reps)): #if both validity conditions have occurred fewer than 3 times, randomly choose which one is next
                p=np.random.random()
                if p >.5:
                    thisValid=0.5
                else:
                    thisValid=0.8
            elif (valid_count.count(0.5)>=(num_reps)) and (valid_count.count(0.8)<(num_reps)): #else choose the one that has not yet occurred 3 times 
                thisValid=0.8
            elif (valid_count.count(0.5)<(num_reps)) and (valid_count.count(0.8)>=(num_reps)):
                thisValid=0.5
        
        valid_count.append(thisValid)
        
        trialDataList=[]
        
        if block==0 and cue != 'neutral': #if this is the first block of this cue type, we want to give them a practice round first
            for circ in stimuli:
                circ.opacity=0
            thisBlock={'cue':cue,'validity':0.5}
            prac_intro1=visual.TextStim(win,pos=[0,.5],units='norm',text='We will begin with a practice block of the task you are about to perform. This round the cue will be a %s cue.'%cue)
            prac_intro2=visual.TextStim(win,pos=[0,0],units='norm',text='Keep in mind that cue accuracy in this practice round will be 50 percent, however this may vary throughout the actual task.')
            prac_intro3=visual.TextStim(win,pos=[0,-.5],units='norm',text='You will always be informed what the cue type and accuracy is before beginning a block. Press any key to start the practice round')
            prac_intro1.draw()
            prac_intro2.draw()
            prac_intro3.draw()
            win.update()
            event.waitKeys()
            pracCond(thisBlock)
            prac_intro4=visual.TextStim(win,pos=[0,.5],units='norm',text='Now we will do the same practice but with a different cue accuracy')
            prac_intro5=visual.TextStim(win,pos=[0,0],units='norm',text='Keep in mind that cue accuracy in this practice round will be 80 percent, however this may vary throughout the actual task')
            prac_intro6=visual.TextStim(win,pos=[0,-.5],units='norm',text='You will always be informed what the cue type and accuracy is before beginning a block. Press any key to start the practice round')
            prac_intro4.draw()
            prac_intro5.draw()
            prac_intro6.draw()
            thisBlock={'cue':cue,'validity':0.8}
            win.update()
            event.waitKeys()
            pracCond(thisBlock)
        elif block==0 and cue=='neutral':
            for circ in stimuli:
                circ.opacity=0
            thisBlock={'cue':cue,'validity':0.0}
            prac_intro1=visual.TextStim(win,pos=[0,.5],units='norm',text='We will begin with a practice block of the task you are about to perform. This round the cue will be a %s cue.'%cue)
            prac_intro2=visual.TextStim(win,pos=[0,0],units='norm',text='Keep in mind that cue accuracy in this practice round will be 0 percent, meaning completely randomized, however this may vary throughout the actual task.')
            prac_intro3=visual.TextStim(win,pos=[0,-.5],units='norm',text='You will always be informed what the cue type and accuracy is before beginning a block. Press any key to start the practice round')
            prac_intro1.draw()
            prac_intro2.draw()
            prac_intro3.draw()
            win.update()
            event.waitKeys()
            pracCond(thisBlock)
        thisBlock=stimList[stimList.index({'cue':cue,'validity':thisValid})]
        
        for n in range(num_trials):

            ITI=make_ITI(expInfo['COMPUTER (b,e,d,m)'])
    
    
            # info for this block --for subject ######################################

            if n==0:
    
                for circs in stimuli:
    
                    circs.opacity = 0 
    
                info_msg=visual.TextStim(win, pos=[0,.5],units='norm',text='This block will show %s cues' %thisBlock['cue']) 
    
                info_msg.draw()
    
                info_msg2=visual.TextStim(win, pos=[0,-.5], units='norm',text='Press any key to continue')
    
                info_msg2.draw()
    
                info_msg3=visual.TextStim(win,pos=[0,0],units='norm',text='The cued locations in this block will be predictive %.1f percent of the time' %(int(thisBlock['validity']*100)))
    
                info_msg3.draw()
    
                win.update()
    
                key1=event.waitKeys()
                
                if key1 and key1[0]=='escape':
                    win.close()
                    core.quit()
                
    
                draw_fixation()
    
                win.flip()
    
                core.wait(3)# pre-block pause
    
            
    
            for circs in stimuli:
    
                circs.opacity=1
    
                circs.setLineColor([0,0,0])
    
                circs.setFillColor([0,0,0])
    
            
    
            if not flex_cond_flag: # if the block is BLOCKED
    
                if n==0: #and its the first trial
    
                    # randomly select two circles to cue
    
                    cue_target_1=np.random.choice(right_stim,1) # SORRY that I named these stupidly-- the cues are not always cueing the target!
    
                    cue_target_2=np.random.choice(left_stim,1)
    
            else: #otherwise, select a new circle every time
    
                cue_target_1=np.random.choice(right_stim,1)
    
                cue_target_2=np.random.choice(left_stim,1)

            #ensure that cue'd circles don't end up too close to each other, ie at clock positions 12 and 1, or 6 and 7
            if no_stim==12:
                while (((cue_target_1[0] is noon)and(cue_target_2[0] is one_oclock)) or ((cue_target_2[0] is noon)and(cue_target_1[0] is one_oclock))) or (((cue_target_1[0] is six_oclock)and(cue_target_2[0] is seven_oclock)) or ((cue_target_2[0] is six_oclock)and(cue_target_1[0] is seven_oclock))):
        
                    cue_target_1=np.random.choice(right_stim,1)
        
                    cue_target_2=np.random.choice(left_stim,1)
    
            color_ind=cue_types_scramble.index(thisBlock['cue'])
            cue_target_1[0].setLineColor(colors_scramble[color_ind])
            cue_target_2[0].setLineColor(colors_scramble[color_ind])
    
#            if thisBlock['cue']=='target':
#                cue_target_1[0].setLineColor([-1,1,-1])
#        
#                cue_target_2[0].setLineColor([-1,1,-1])
#            elif thisBlock['cue']=='distractor': # some other color than green. blue?
#                cue_target_1[0].setLineColor([0,0,1])
#        
#                cue_target_2[0].setLineColor([0,0,1])
#            elif thisBlock['cue']=='neutral': # yellow?
#                cue_target_1[0].setLineColor([1,1,0])
#        
#                cue_target_2[0].setLineColor([1,1,0])
            
            if EEGflag:
                port.close()
                port.open()
                #win.callonFlip(pport.setData,delay1trig)
                port.write(delay1trig)
                port.flush()
                wait_here(.2)
                port.close()
            
            
            #win.flip()
            wait_here(.5)
            #core.wait(.5) # CUE PERIOD #################################################
            
            if EEGflag:
                port.open()
                if thisBlock['cue']=='target':
                    if thisBlock['validity']==0.5:
                        #win.callonFlip(pport.setData,target5trig)
                        port.write(target5trig)
                    elif thisBlock['validity']==0.8:
                        #win.callonFlip(pport.setData,target8trig)
                        port.write(target8trig)
                elif thisBlock['cue']=='distractor':
                    if thisBlock['validity']==0.5:
                        #win.callonFlip(pport.setData,dis5trig)
                        port.write(dis5trig)
                    elif thisBlock['validity']==0.8:
                        #win.callonFlip(pport.setData,dis8trig)
                        port.write(dis8trig)
                elif thisBlock['cue']=='neutral':
                    #win.callonFlip(pport.setData,neutraltrig)
                    port.write(neutraltrig)
                port.flush()
                wait_here(.2)
                port.close()
    
            # ## SOA period
    
            for circs in stimuli:
    
                circs.setLineColor([0,0,0])
            

            #win.flip()
    
            wait_here(1.5)
            #core.wait(1.5) # DELAY #####################################################
    
            draw_fixation()
    
            target_loc1 = list(right_stim).index(cue_target_1[0]) #where are the two cued circles?
    
            stim_minus_one = np.delete(right_stim, target_loc1) 
    
            target_loc2 = list(left_stim).index(cue_target_2[0]) 
    
            stim_minus_two = np.delete(left_stim,target_loc2) #get a list of stimuli that don't include cued circles
    
            stim_minus_both=list(stim_minus_one)+list(stim_minus_two)
    
            
    
            if thisBlock['validity']==.5: # THIS GIVES HALF THE CHANCE TO EITHER CUED SPOT, SO ANY ONE CUED SPOT HAS .25 or .40 chance of selection
    
                which_circle= np.random.choice([cue_target_1[0], cue_target_2[0], stim_minus_both],1,p=[0.25,0.25,0.5]) #decide if cue is valid, using validity % of this condition
    
            elif thisBlock['validity']==.8:
    
                which_circle= np.random.choice([cue_target_1[0], cue_target_2[0], stim_minus_both],1,p=[0.4,0.4,0.2]) # FIX THIS??? should stim_minus_two be changed ??
   
    
            if thisBlock['cue']=='neutral':#since the neutral cue is neutral, it isn't going to be valid and targets/distractors will be randomly assigned
    
                trial_type= 'None' 
                cue_side='None'
    
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
    
                        distractor_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos #make sure the dist goes in a non-cued location
    
                    else:
    
                        distractor_stim.pos= (np.random.choice(stim_minus_two,1))[0].pos
    
                
    
                else: #if this trial is invalid 
                    probe1=np.random.choice(stim_minus_one,1,replace=False) #select two circles that aren't the cued circles
                    probe2=np.random.choice(stim_minus_two,1,replace=False)

                    tarNdist=np.random.choice([probe1[0],probe2[0]],2,replace=False) #then randomly  assign the target to one and dist to another
                    distractor_stim.pos=tarNdist[0].pos 
                    target_stim.pos=tarNdist[1].pos
        
#                        tar=np.random.choice(stim_minus_one,1,replace=False) #select two circles that aren't the cued circles
#                        dist=np.random.choice(stim_minus_two,1,replace=False)
#                        distractor_stim.pos=dist[0].pos #put the distractor in one and the target in the other
#                        target_stim.pos=tar[0].pos

    
            elif thisBlock['cue']=='distractor':
    
                if trial_type=='valid': #if this trial's cued locations are valid, put the distractor in one of them
    
                    distractor_stim.pos=which_circle[0].pos
    
                    if cue_side=='L': #if the dist is on the Left side of the clock, we want the target on the right and vice versa
    
                        target_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos
    
                    else:
    
                        target_stim.pos= (np.random.choice(stim_minus_two,1))[0].pos
    
                else:
    
                    if TarindistFlag and (np.random.choice([True,False],1,p=[.10,.90])[0]): #if the trial's cued location is invalid AND we want a target in a distractor-cued loc
    
                        #we only want a target in a dist cued loc once in a while (10% of all invalid trials)
                        tarinDistloc=np.random.choice([cue_target_1[0],cue_target_2[0]],1) #randomly choose the left or right cue to put it in
                        target_stim.pos=tarinDistloc[0].pos #put the target in the chosen 'distractor' circle
                        
                        if tarinDistloc[0]==cue_target_1[0]:
                            cue_side=='R'
                        else:
                            cue_side=='L'
                        trial_tarInDist=1
                        if EEGflag:
                            port.open()
                            #win.callonFlip(pport.setData,tIdtrig) # will this overwrite the probe flag?
                            port.write(tIdtrig)
                            port.flush()
                            wait_here(.2)
                            port.close()
    
                        if cue_side=='L':
    
                            distractor_stim.pos=(np.random.choice(stim_minus_one,1))[0].pos #put the distractor on the opposite side of the target
    
                        else:
    
                            distractor_stim.pos=(np.random.choice(stim_minus_two,1))[0].pos
    
                    else:
    
                        probe1=np.random.choice(stim_minus_one,1,replace=False) #select two circles that aren't the cued circles
    
                        probe2=np.random.choice(stim_minus_two,1,replace=False)
    
                        tarNdist=np.random.choice([probe1[0],probe2[0]],2,replace=False) #them randomly assign the target to one and dist to another
    
                        distractor_stim.pos=tarNdist[0].pos 
    
                        target_stim.pos=tarNdist[1].pos
    
            
    
            elif thisBlock['cue']=='neutral':
    
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
    
            
    
            for circs in stimuli: 
    
                if not (((circs.pos[0]==target_stim.pos[0]) and (circs.pos[1]==target_stim.pos[1])) or ((circs.pos[0]==distractor_stim.pos[0]) and (circs.pos[1]==distractor_stim.pos[1]))): #if the circle isn't a target or distractor, its grey
    
                    circs.setLineColor([0,0,0])
    
                    circs.setFillColor(None)
    
                else:
    
                    circs.setLineColor([1,-1,-1])
    
                    circs.setFillColor(None)
    
            
    
            win.update()
    
            
    
            clock=core.Clock()
    
            subResp= event.waitKeys(1.5,keyList=['up','down','left','right'],timeStamped=clock)
    
            if subResp==None:
    
                trial_corr=-1
    
                RT=-1
    
                key='None'
    
            else:
    
                if subResp[0][0]==corrKey:
    
                    trial_corr=1
    
                else:
    
                    trial_corr=0
    
                RT=subResp[0][1]
    
                key=subResp[0][0]
    
            if EEGflag:
                port.open()
                #win.callonFlip(pport.setData,probetrig)
                port.write(probetrig)
                port.flush()
                wait_here(.2)
                port.close()
    
            #core.wait(0) # PROBE AND RESP ############################################## 
    
            for circs in stimuli:
    
                circs.setLineColor([0,0,0])
    
                circs.setFillColor([0,0,0])
    
            
    
            #this my have to be rounded up or down depending on refresh rate? see: https://discourse.psychopy.org/t/jittering-iti-by-code-in-the-builder/4116
    
            #ITI=round(1,ITI)
    
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
    
            
    
            #event.clearKeys()
    
            key=event.getKeys()
            
    
            if key: 
                if (expInfo['COMPUTER (b,e,d,m)']=='b' or expInfo['COMPUTER (b,e,d,m)']=='m') and key[0]=='escape': #for the EEG stim presentation on the dell or mac in Dillan's office
                    win.close()
                    core.quit()
                elif expInfo['COMPUTER (b,e,d,m)']=='d'and key[0]=='Esc': # for dillan's laptop--key responses seem to be different?
                    win.close()
                    core.quit()
                print('FORCED QUIT')
    
          
            if EEGflag:
                port.open()
                #win.callonFlip(pport.setData,ITItrig)
                port.write(ITItrig)
                port.flush()
                wait_here(.2)
                port.close()
            #win.flip()
            wait_here(ITI)
            #core.wait(ITI) #ITI--want to jitter this?, with an average of 4 seconds
            
    #        if n==num_trials:
    #            continue_msg=visual.TextStim(win,pos=[0,0],units='norm',text='Done with this block. Continue to the next? (y, n, or escape)' )
    #            continue_msg.draw()
    #            win.update()
    #            key=event.waitKeys(keyList=['y','n','escape'])
    #            if key=='n':
    #                continue_msg2=visual.TextStim
        
        blocks.update({'blockInfo_%i%s'%(block,cue):{'block':k,'cueType':thisBlock['cue'],'validity':thisBlock['validity'],'trialsData':trialDataList}})
        # #########################saving data out###########################################
        make_csv(filename)
        k=k+1

if EEGflag:
    port.close()
    port.open()
    #win.callonFlip(pport.setData,delay1trig)
    port.write(stopSaveflag)
    port.flush()
    wait_here(.2)
    port.close()
print('\n\n')

print(blocks)

