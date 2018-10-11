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

import csv



#testing github

# Ensure that relative paths start from the same directory as this script

_thisDir = os.path.dirname(os.path.abspath(__file__))

os.chdir(_thisDir)



# Store info about the experiment session

expName = 'alpha_pilot'  # from the Builder filename that created this script

expInfo = {'subject': '', 'session': '01','f or b?':'f','no stim':'12','t in d?':'n', 'lat?':'n','COMPUTER (b,e,d,m)':'b'}

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



#endExpNow = False  # flag for 'escape' or other condition => quit the exp



# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc

filename = _thisDir + os.sep + u'data/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])



# ###############Flags####################################################################################



# this is where we'll flag the different piloted conditions



#will blocks be flexbile or predictable?

if expInfo['f or b?']=='f':

    flex_cond_flag = True

else:

    flex_cond_flag = False



#number of cue locations

no_stim = float(expInfo['no stim'])



# distractor in target location condition?

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
    target_stim=visual.ImageStim(win, image='C:\Stimuli\T2.png') #size=([.5,.5]
    distractor_stim=visual.ImageStim(win, image='C:\Stimuli\I3.png') #behavioral stimulus presentation Dell
elif expInfo['COMPUTER (b,e,d,m)']=='d':
    target_stim=visual.ImageStim(win, image='C:\\Users\\dillc\\Downloads\\T2.png')
    distractor_stim=visual.ImageStim(win, image='C:\\Users\\dillc\\Downloads\\I3.png') #dillan's computer


cue_types=['target','distractor'] # distractor or target or neutral cues



cue_valid=[.5,.8] # cue validity



num_trials=33 # change later to 33



stimList=[]

for cue in cue_types:

    for num in cue_valid:

        stimList.append({'cue':cue,'validity':num})

stimList.append({'cue':'neutral','validity':0})



print(stimList)

# ####stimulus##############################################################################################



from psychopy import visual, core

win = visual.Window([1680,1050],units='deg',fullscr=False,monitor='testMonitor')



def draw_fixation(): #0 to 1, for the opacity

    fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))

    fixation.size=0.6

    #fixation.opacity=n

    fixation.draw()

    win.update

    

#fixation.setAutoDraw(True)



intro_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Welcome to the experiment!')

intro_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='You will see a series of circles that will indicate the location of the target "T" or of the distractor "I" some portion of the time')

intro_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Press any key to continue')

intro_msg.draw()

intro_msg2.draw() 

intro_msg3.draw()



win.flip()

event.waitKeys()



intro_mesg4= visual.TextStim(win,pos=[0,.5],units='norm',text='Please remain focused on the cross in the middle of the screen at all times')

intro_mesg5=visual.TextStim(win,pos=[0,0], units='norm',text='Respond to the orientation of the capital "T" using the arrow keys on the keyboard')

intro_mesg6=visual.TextStim(win,pos=[0,-0.5],units='norm',text='You will also see a capital "I." Do NOT respond to the orientation of the I. Press any key to continue.')

intro_mesg4.draw()

intro_mesg5.draw()

intro_mesg6.draw()



win.flip()

event.waitKeys()



draw_fixation()

win.flip()

vis_deg=2

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

        size=(.09,0.15),  

        lineWidth=7, lineColor=None, fillColor=None,

        pos=(0.0,-2))

    six_oclock.setAutoDraw(True)

    eleven_oclock = visual.Circle(

        win=win, name='11',

        size=(0.09, 0.15),

        ori=0, pos=(-1, ((sqrt(3)/2)*2)),

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



for stim in stimuli:

    stim.size=(0.70,0.70)
distractor_stim.size=([.5,.5])
target_stim.size=([.5,.5])



# ############################################blocks#######################################

# print(stimList)



blocks=data.TrialHandler(stimList,3,method='random')#one repeats each, randomly assorted but each cond is completed before they recycle #change to 3



k=0

for thisBlock in blocks:

    

    trialDataList=[]

    #cue_target=[]

    for n in range(num_trials):

        ITI=np.random.uniform(3.8,4.5)

        

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

                cue_target_1=np.random.choice(stimuli[:6],1)

                cue_target_2=np.random.choice(stimuli[6:],1)

        else: #otherwise, select a new circle every time

            cue_target_1=np.random.choice(stimuli[:6],1)

            cue_target_2=np.random.choice(stimuli[6:],1)



        #ensure that cue'd circles don't end up too close to each other, ie at clock positions 12 and 1, or 6 and 7

        while ((cue_target_1[0] is noon)and(cue_target_2[0] is one_oclock)) or ((cue_target_1[0] is six_oclock) and (cue_target_2[0] is seven_oclock)):

            cue_target_1=np.random.choice(stimuli[:6],1)

            cue_target_2=np.random.choice(stimuli[6:],1)



        cue_target_1[0].setLineColor([-1,1,-1])

        cue_target_2[0].setLineColor([-1,1,-1])

        

        win.flip()

        core.wait(.5) # CUE PERIOD #################################################

        

        draw_fixation()

        # ## SOA period

        for circs in stimuli:

            circs.setLineColor([0,0,0])

        

        win.flip()

        core.wait(1.5) # DELAY #####################################################

        

        draw_fixation()

        

        target_loc1 = list(stimuli[:6]).index(cue_target_1[0]) #where are the two cued circles?

        stim_minus_one = np.delete(stimuli[:6], target_loc1) 

        target_loc2 = list(stimuli[6:]).index(cue_target_2[0]) 

        stim_minus_two = np.delete(stimuli[6:],target_loc2) #get a list of stimuli that don't include cued circles

        

        

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

                    distractor_stim.pos=(np.random.choice(stimuli[:6],1))[0].pos

                else:

                    distractor_stim.pos= (np.random.choice(stimuli[6:],1))[0].pos



            else: #if this trial is invalid 

                    tar=np.random.choice(stim_minus_one,1,replace=False) #select two circles that aren't the cued circles

                    dist=np.random.choice(stim_minus_two,1,replace=False)

                    distractor_stim.pos=dist[0].pos #put the distractor in one and the target in the other

                    target_stim.pos=tar[0].pos

    

        elif thisBlock['cue']=='distractor':

            

            if trial_type=='valid': #if this trial's cued locations are valid, put the distractor in one of them

                distractor_stim.pos=which_circle[0].pos

                if cue_side=='L': #if the dist is on the Left side of the clock, we want the target on the right and vice versa

                    target_stim.pos=(np.random.choice(stimuli[:6],1))[0].pos

                else:

                    target_stim.pos= (np.random.choice(stimuli[6:],1))[0].pos

            

            else:

                if TarindistFlag and (np.random.choice([True,False],1,p=[.10,.90])[0]): #if the trial's cued location is invalid AND we want a target in a distractor-cued loc

                    #we only want a target in a dist cued loc once in a while (10% of all invalid trials)

                    target_stim.pos=which_circle[0].pos #put the target in the chosen 'distractor' circle

                    trial_tarInDist=1

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

            trial_corr=0

            RT='None'

            key='None'

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

        

        Thistrial_data= {'trialNum':(n+1),'trial_type':trial_type,'corrResp':corrKey,'subjectResp':key,'trialCorr?':trial_corr,'RT':RT, 'tarinDisCond':trial_tarInDist,'ITI':ITI}

        trialDataList.append(Thistrial_data)

        print(trialDataList)

        

        #event.clearKeys()

        key=event.getKeys()

        if expInfo['COMPUTER (b,e,d,m)']='b':
            
           if key and key[0]=='escape': #for the EEG stim presentation on the dell
                win.close()
                core.quit()

        elif expInfo['COMPUTER (b,e,d,m)']='d':
            
            if key and key[0]=='Esc': # for dillan's comp--key responses seem to be different?
                win.close()
                core.quit()

      

        win.flip()

        core.wait(ITI) #ITI--want to jitter this?, with an average of 4 seconds

    

    blocks.data.add('blockInfo',{'blockNum':k,'cueType':thisBlock['cue'],'validity':thisBlock['validity'],'trialsData':trialDataList})

    k=k+1

    

# #########################saving data out###########################################



with open(filename+'.csv', mode='w') as csv_file:

    fieldnames=['flex or blocked?','no stim','TarInDistFlag','lateralized?','block','cue','validity','trialNum','trial_type','corrResp','subResp','trialCorr?','RT','tarinDisCond','ITI']

    #fieldnames is simply asserting the categories at the top of the CSV

    writer=csv.DictWriter(csv_file,fieldnames=fieldnames)

    writer.writeheader()

    

    writer.writerow({'flex or blocked?': flex_cond_flag,'no stim':expInfo['no stim'],'TarInDistFlag':TarindistFlag,'lateralized?':lat_stim_flag})
    #This is just to give info about the session overall: was the session blocked or flexibly cued? How many stim? etc.

    print('\n\n\n')
    #print(blocks.data['blockInfo'])

    cond_data=blocks.data['blockInfo'] #the data structure made by trialHandler seems to group conditions together in seperate lists. Want to access them one by one
    print(len(cond_data))  # how many conditions? should be 5
    for n in range(len(cond_data)): # loop through each condition
        blocks_data = cond_data[n]
        
        for n in range(len(blocks_data)): #loop through each block of that condition
            #print('\n\n\n')
    
            ThisBlock=blocks_data[n] #grabbing the block info out of data for this block
            #print(ThisBlock)
            #print('\n')
    
            for k in range(len(ThisBlock['trialsData'])): #this should be the # of trials
                ThisTrial=ThisBlock['trialsData'][k] #grabbing the trial info out of data for this trial
                #print(ThisTrial)
                if k==0: #if it's the first trial i want the block info written next to it. Otherwise, this column should be blank
    
                    writer.writerow({'block':ThisBlock['blockNum'],'cue':ThisBlock['cueType'],'validity':ThisBlock['validity'],
    
                                    'trialNum':ThisTrial['trialNum'],'trial_type':ThisTrial['trial_type'],
    
                                    'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
    
                                    'RT':ThisTrial['RT'],'tarinDisCond':ThisTrial['tarinDisCond'],
    
                                    'ITI':ThisTrial['ITI']})
    
                else:
    
                    writer.writerow({'block':'','cue':'','validity':'',
    
                                    'trialNum':ThisTrial['trialNum'],'trial_type':ThisTrial['trial_type'],
    
                                    'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
    
                                    'RT':ThisTrial['RT'],'tarinDisCond':ThisTrial['tarinDisCond'],
    
                                    'ITI':ThisTrial['ITI']})
            #print('\n\n\n')