
# updates 10/30/19: CHANGED TO MATCH BRAD's FOR EEG--  changed colors, changed when oriented bars appear, changed response mapping
#   change probe back to two seconds, add two shapes so that there are 8 shapes, ratio of trials is 1/3 1/3 1/3 t/d/n, and one long soa (1000ms) and one short soa (100ms). Changed practice to all neutrals
# updates 06/13/19: added new colors and .png bars
# updates 05/21/19: changing paradigm so that we have placeholders and target/distractor associated colors 
# updates 05/28/19: orientation of bars should be half vertical, half horizontal, put them in placeholders, timeout when inaccurate, add a neutral condition! no singleton

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

expInfo = {'subject': '', 'session': '01','EEG? [y/n]':'n','refresh':50,'block':1,'color_code [1-6]':''}
expName='alpha_placeholders_matchingBrad'
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
win = visual.Window([1240,1024],units='deg',fullscr=True,monitor='testMonitor',checkTiming=True,colorSpace='rgb255',color=[0,0,0])
no_stim=8
vis_deg=4.66#3.5#*10 

blockNum=int(expInfo['block'])

if expInfo['color_code [1-6]'] not in ['1','2','3','4','5','6']:
    print( 'PLEASE ENTER A VALID COLOR CODE')
    core.quit()

for key in ['escape']:
    event.globalKeys.add(key, func=core.quit)

if expInfo['EEG? [y/n]']=='y':
    EEGflag=1
else:
    EEGflag=0

if EEGflag:
    port=serial.Serial('COM6',baudrate=115200)
    port.close()
    startSaveflag=bytes([201])
    startBlockflag=bytes([133])
    stopBlockflag=bytes([135])
    stopSaveflag=bytes([255])
    cue_trigDict={'dis_short_cue_trig': 101,
                  'dis_long_cue_trig':103,
                  'tar_short_cue_trig':105,
                  'tar_long_cue_trig':107,
                  'neut_short_cue_trig':109,
                  'neut_long_cue_trig':111}
    
    probe_trigDict={'dis_short_probe_trig': 113,
                  'dis_long_probe_trig':115,
                  'tar_short_probe_trig':117,
                  'tar_long_probe_trig':119,
                  'neut_short_probe_trig':121,
                  'neut_long_probe_trig':123}
    
    other_trigDict={'grey_placeholders_trig':125, 'ITI_trig':127,'subNonRespTrig':129,'subRespTrig':131}

if EEGflag:
    filename='Z:/AlphaStudy_Data/eegData/eeg_behavior_data'+u'/%s_%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['block'],expInfo['date'])
else:
    filename='Z:/AlphaStudy_Data/behavData'+u'/%s_%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['block'],expInfo['date']) #for dells
    #filename='/Volumes/rdss_kahwang/AlphaStudy_Data/behavData'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])

refresh_rate=expInfo['refresh']

num_trials=60 #has to be divisible by 6, will yield (num_trials/6) trials per condition for each block
num_blocks=1#10


#trialNum':(n),'tarVorI':tarVorI,'disCue_type':disCue_type,'dPOA':dPOA,'disVorI':disVorI,'distractor_loc':loc,'corrResp':corrKey
#blocks.update({'blockInfo_%i'%(block):{'block':block,'tarCue':thisBlock[0],'disCue':thisBlock[1],'highProbLoc?':disProb,'likely_dis':saveDis,'likelyDisHemisphere':disHemi,'trialsData':trialDataList}})

def pracCond(n_practrials=9,demo=False):
    pracDataList=[]
    pracBlock=[]
    for r in range(int(n_practrials)):
        #pracBlock.append('dis')
        #pracBlock.append('tar')
        pracBlock.append('neut')
    for n in range(n_practrials):
        ITI=1.5
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
        for i in range(no_stim):
            shape=stimuli[i]
            grey_placeholder_circs[i].pos=shape.pos
            grey_placeholder_diamonds[i].pos=shape.pos
            grey_placeholder_circs[i].autoDraw=True
            grey_placeholder_diamonds[i].autoDraw=True
        wait_here(.5)
        for greys in grey_placeholder_circs:
            greys.autoDraw=False
        for greys in grey_placeholder_diamonds:
            greys.autoDraw=False        
        distractor_stim,target_stim,other_stim,other_placeholders,tar_placeholder,dis_placeholder=generate_target(tar_cue_color,dis_cue_color,pracBlock[n])
        ITI=make_ITI()
        print(pracBlock[n])
        cue_circs=np.random.choice(stimuli,2, replace=False)
        dis_circ=cue_circs[0]
        tar_circ=cue_circs[1]
        target_stim.pos=tar_circ.pos
        tar_placeholder.pos=tar_circ.pos
        distractor_stim.pos=dis_circ.pos
        dis_placeholder.pos=dis_circ.pos
        target_stim.autoDraw=True
        distractor_stim.autoDraw=True
        dis_placeholder.autoDraw=True
        tar_placeholder.autoDraw=True
        for i in range(no_stim):
            shape=stimuli[i]
            if shape != tar_circ and shape!=dis_circ:
                #other_stim[i].pos=shape.pos
                other_stim[i].autoDraw=True
                other_placeholders[i].autoDraw=True
        fixation.autoDraw=True
        wait_here(1.5) # ############## Cue presentation ###################
        fixation.autoDraw=True
        for o in other_placeholders: o.autoDraw=False
        for a in other_stim: a.autoDraw=False
        target_stim.autoDraw=False
        distractor_stim.autoDraw=False
        dis_placeholder.autoDraw=False
        tar_placeholder.autoDraw=False
        #wait_here(SOA) # ############ delay one/SOA period ###############
        distractor_stim.autoDraw=True
        target_stim.autoDraw=True
        for i in range(no_stim):
            shape=stimuli[i]
            if shape != tar_circ and shape!=dis_circ:
                #other_stim[i].pos=shape.pos
                other_stim[i].autoDraw=True
        bar_oris=np.random.permutation([0,0,0,0,90,90,90,90])
        for s in range(len(stimuli)):
            circs=stimuli[s]
            bars[s].pos=other_stim[s].pos #except target and distractor
            bars[s].ori=bar_oris[s]
            bars[s].autoDraw=True
            if circs==tar_circ:
                target_ori=bars[s].ori #then document the orientation of the bar at this loc
                print(target_ori)
        if target_ori==0:
            corrKey='q'#'up'
        elif target_ori==90:
            corrKey='p'
        #wait_here(2) # ############### probe presentation ####################
        event.clearEvents()
        max_win_count=int(3/(1/refresh_rate))
        win_count=0
        subResp=None
        clock=core.Clock()
        while not subResp:
            win.flip()
            subResp=event.getKeys(keyList=['q','p'], timeStamped=clock)
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
            elif subResp[0][0] != corrKey:
                trial_corr=0
            RT=subResp[0][1]
            key=subResp[0][0]
        print(subResp)
        pracDataList.append(trial_corr)
        fixation.draw()
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

        fieldnames=['tar_color','dis_color','SOA','block','trialNum','trial_type','corrResp','subResp','trialCorr?','RT','tar,dis stim_loc','ITI','Tar,Dis,Other','trial_trigs','triggers']
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
                
                if EEGflag:
                    writer.writerow({'tar_color':tar_cue_color,'dis_color':dis_cue_color,'SOA':ThisTrial['SOA'],
                                    'block':ThisBlock['block'],'trialNum':ThisTrial['trialNum'],'trial_type':ThisTrial['trial_type'],
                                    'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                    'RT':ThisTrial['RT'],'tar,dis stim_loc':ThisTrial['tar,dis stim_loc'],
                                    'ITI':ThisTrial['ITI'],'Tar,Dis,Other':ThisTrial['Tar,Dis,Other'],'trial_trigs':ThisTrial['trial_trigs'],'triggers':(cue_trigDict,probe_trigDict,other_trigDict)})
                else:
                    writer.writerow({'tar_color':tar_cue_color,'dis_color':dis_cue_color,'SOA':ThisTrial['SOA'],
                                    'block':ThisBlock['block'],'trialNum':ThisTrial['trialNum'],'trial_type':ThisTrial['trial_type'],
                                    'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                    'RT':ThisTrial['RT'],'tar,dis stim_loc':ThisTrial['tar,dis stim_loc'],
                                    'ITI':ThisTrial['ITI'],'Tar,Dis,Other':ThisTrial['Tar,Dis,Other'],'trial_trigs':ThisTrial['trial_trigs'],'triggers':''})
if no_stim==8:
    noon_oclock = visual.Circle(

        win=win, name='12',

        size=(0.09, 0.15),

        ori=0, pos=(0, vis_deg),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=0.0, interpolate=True)

    noon_oclock.setAutoDraw(True)
    one_oclock = visual.Circle(
    
            win=win, name='1',
    
            size=(0.09, 0.15),
    
            ori=0,  pos=(vis_deg*(sqrt(2)/2), ((sqrt(2)/2)*vis_deg)),
    
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

        ori=0, pos=(vis_deg*(sqrt(2)/2), -((sqrt(2)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-5.0, interpolate=True)

    five_oclock.setAutoDraw(True)
    six_oclock = visual.Circle(

        win=win, name= '6', 

        size=(.09,0.15),  ori=0, pos=(0, -vis_deg),

        lineWidth=7, lineColor=None, fillColor=None)

    six_oclock.setAutoDraw(True)
    seven_oclock = visual.Circle(

        win=win, name='7',

        size=(0.09, 0.15),

        ori=0, pos=(-vis_deg*(sqrt(2)/2), -((sqrt(2)/2)*vis_deg)),


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

        ori=0, pos=(-vis_deg*(sqrt(2)/2), ((sqrt(2)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-1.0, interpolate=True)

    eleven_oclock.setAutoDraw(True)
    stimuli=[noon_oclock,one_oclock,three_oclock,five_oclock,six_oclock,seven_oclock,nine_oclock,eleven_oclock]
    right_stim=stimuli[:4]
    left_stim=stimuli[4:]

diamond_size=(4.66,3.6)#(3.7,2.9)
circ_size=(4.66,3.6)#(3.5,2.7) #(.2,.2)
#size=(3.2,2.5)
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
grey_placeholder_circs=[visual.ImageStim(win=win,image=images['grey_circle'].image, units='deg',ori=0,size=images['grey_circle'].size,name='grey_circle') for i in range(no_stim)]
grey_placeholder_diamonds=[visual.ImageStim(win=win,image=images['grey_diamond'].image, units='deg',ori=0,size=images['grey_diamond'].size,name='grey_diamond') for i in range(no_stim)]
images_names=list(images.keys())
colors=['blue','red','pink']
#dis_tar_colors=np.random.choice(colors,2,replace=False)
#tar_cue_color=dis_tar_colors[0]
#dis_cue_color=dis_tar_colors[1]
if expInfo['color_code [1-6]']=='1':
    tar_cue_color='red'
    dis_cue_color='blue'
elif expInfo['color_code [1-6]']=='2':
    tar_cue_color='red'
    dis_cue_color='pink'
elif expInfo['color_code [1-6]']=='3':
    tar_cue_color='blue'
    dis_cue_color='red'
elif expInfo['color_code [1-6]']=='4':
    tar_cue_color='blue'
    dis_cue_color='pink'
elif expInfo['color_code [1-6]']=='5':
    tar_cue_color='pink'
    dis_cue_color='red'
elif expInfo['color_code [1-6]']=='6':
    tar_cue_color='pink'
    dis_cue_color='blue'

neutral_colors=['green']#[color for color in colors if (color != tar_cue_color and color != dis_cue_color)]
print(tar_cue_color)
print(dis_cue_color)
print(neutral_colors)

def generate_target(target_color,distractor_color ,cue_type):
    
    shapes=np.random.choice(['diamond','circle'],2,replace=False)
    distractor_shape=shapes[0]
    target_shape=shapes[1]
    other_shape=distractor_shape 
    if cue_type=='dis':
        distractor_stim=images[distractor_color+'_'+distractor_shape] #the singleton distractor (same shape as non singleton distractors)
        dis_placeholder=images[distractor_color+'_'+target_shape] # the shape that is not the distractor shape to be overlaid during the cue period
        neutral_color=np.random.choice(neutral_colors,1)[0]
        target_stim=images[neutral_color+'_'+target_shape] #the target shape 
        other_name=neutral_color+'_'+other_shape #the non singleton distractor (same shape as singleton distractor)
        other_placeholder_name=neutral_color+'_'+target_shape #the non singleton distractor color plus the shape of the target to overlay during placeholder cue
        tar_placeholder=images[other_name]
    elif cue_type=='tar':
        target_stim=images[target_color+'_'+target_shape]
        tar_placeholder=images[target_color+'_'+other_shape] # the non-target shape overlaid with the target during the placeholder cue
        neutral_color=np.random.choice(neutral_colors,1)[0]
        other_name=neutral_color+'_'+other_shape
        other_placeholder_name=neutral_color+'_'+target_shape
        distractor_stim=images[other_name] #basically there's no distractor on tar cue trials, so assigning this var name to the Other_stim for simplicity 
        dis_placeholder=images[other_placeholder_name]
    elif cue_type=='neut':
        neutral_color=np.random.choice(neutral_colors,1)[0]
        other_placeholder_name=neutral_color+'_'+target_shape
        other_name=neutral_color+'_'+other_shape
        target_stim=images[other_placeholder_name]
        distractor_stim=images[other_name] #the 'other' shapes and the distractor shape are the same thing on neutral trials
        dis_placeholder=visual.ImageStim(win=win,image=images[other_placeholder_name].image, units='deg',ori=0,size=images[other_placeholder_name].size,name=other_placeholder_name)
        tar_placeholder=visual.ImageStim(win=win,image=images[other_name].image, units='deg',ori=0,size=images[other_name].size,name=other_name)
        # have to construct a new object on neutral trials for tar_placeholder bc this stim is being used more than once
    
    other_placeholders=[visual.ImageStim(win=win,image=images[other_placeholder_name].image, units='deg',ori=0,size=images[other_placeholder_name].size,name=other_placeholder_name) for i in range(no_stim)]
    other_stim=[visual.ImageStim(win=win,image=images[other_name].image, units='deg',ori=0,size=images[other_name].size,name=other_name) for i in range(no_stim)] # making 4 copies of Other_shape 
    for g in range(no_stim):
        #other_stim[g].autoDraw=True
        other_stim[g].pos=(stimuli[g].pos[0],stimuli[g].pos[1])#(stimuli[g].pos[0]/6,stimuli[g].pos[1]/6)#
        #print(stimuli[g].pos)
        other_placeholders[g].pos=(stimuli[g].pos[0],stimuli[g].pos[1])
    
    print(target_stim.name)
    print(distractor_stim.name)
    print(other_stim[0].name)
    
    distractor_stim.opacity=1
    target_stim.opacity=1
    #distractor_stim.autoDraw=True
    #target_stim.autoDraw=True
    return distractor_stim,target_stim,other_stim,other_placeholders,tar_placeholder,dis_placeholder

fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))
fixation.size=0.6

#disc_bar= visual.ImageStim(win=win,name='bar', units='deg', 
#    ori=0,image=os.getcwd()+'/stimuli/Verticle.png')
#visual.TextStim(win, text='|',units='deg', color=(1,1,1))
disc_bar_size=(1.4,1.63)
bars=[visual.ImageStim(win=win,name='bar', units='deg', 
    ori=0,size=disc_bar_size,image=os.getcwd()+'/stimuli/Verticle.png') for i in range(no_stim)]
timeout_msg=visual.TextStim(win,pos=[0,0], units='norm',text='Answer incorrect')

if blockNum==1:
    intro_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Welcome to the experiment!')
    intro_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='You will see a series of layered objects. Some of them will disappear. You must find the SHAPE that is unique. This is the target shape.')#You must find the target shape. The target shape is the %s' % (target_stim.name.split('_')[0])+' '+(target_stim.name.split('_')[1]))
    intro_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Do NOT respond to the COLOR of the objects, only the SHAPES. Press any key to continue')
    intro_msg.draw()
    intro_msg2.draw() 
    intro_msg3.draw()
    win.flip()
    event.waitKeys()
    intro_mesg4= visual.TextStim(win,pos=[0,.5],units='norm',text='Please remain focused on the cross in the middle of the screen whenever there are NOT shapes on the screen.')
    intro_mesg5=visual.TextStim(win,pos=[0,0], units='norm',text='Respond to the orientation of the line in the target shape using the Q AND P keys on the keyboard')
    intro_mesg6=visual.TextStim(win,pos=[0,-0.5],units='norm',text='Press any key to continue.')
    intro_mesg4.draw()
    intro_mesg5.draw()
    intro_mesg6.draw()
    win.flip()
    event.waitKeys()
    instruction_slide1=visual.ImageStim(win=win,image=os.getcwd()+'/instruction_slides/singsearch_placeholder_nomask.png')
    instruction_slide1.draw()
    win.flip()
    event.waitKeys()
    instruction_slide2=visual.ImageStim(win=win,image=os.getcwd()+'/instruction_slides/singsearch_placeholder_colors.png')
    instruction_slide2.draw()
    win.flip()
    event.waitKeys()

SOA_maps={'short':.1,'long':1}
cue_list=['tar','dis','neut']
soa_list=['short','long']

stimList=[] #list of trials
for c in cue_list:
    for s in soa_list:
        for n in range(int(num_trials/(len(cue_list)*len(soa_list)))): # divide trials by the # of conditions, which is the len(cues_list)*len(soa_list), ie 6
            stimList.append([c,s])

stimList_blocks=[] #list of blocks, which contains a list of trials
for n in range(num_blocks): 
    stimList_scramble=list(np.random.permutation(stimList))
    stimList_blocks.append(stimList_scramble)

if EEGflag:
    port.open()
    port.write(startSaveflag)
    print("STARTED THE SAVING")
    #port.close()

blocks={} # where we will save out the data

#pracCond(n_practrials=6,demo=True)
if blockNum==1:
    pracCond(n_practrials=12,demo=False)

if EEGflag:
    port.write(startBlockflag)

for block in range(len(stimList_blocks)):
    
    trialDataList=[]
    
    fixation.color=([0,0,0])
    if block ==0:
        info_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to start the experiment.')
        info_msg2.draw()
        win.flip()
        key1=event.waitKeys()
    else:
        info_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='You are finished with this block. Please call the experimenter in the room.')
        info_msg2.draw()
        win.flip()
        key1=event.waitKeys(keyList=['z'])
    fixation.color=([1,1,1])
    fixation.text='+'
    fixation.draw()
    win.flip() 
    core.wait(3)# pre-block pause
    thisBlock=stimList_blocks[block]
    
    
    for trial in range(len(thisBlock)): # where thisBlock is the length of num trials
        distractor_stim,target_stim,other_stim,other_placeholders,tar_placeholder,dis_placeholder=generate_target(tar_cue_color,dis_cue_color,thisBlock[trial][0])
        ITI=make_ITI()
        print(thisBlock[trial])
        SOA=thisBlock[trial][1]
        
        if EEGflag:
            win.callOnFlip(port.write,bytes([other_trigDict['grey_placeholders_trig']]))
        
        for i in range(no_stim):
            shape=stimuli[i]
            grey_placeholder_circs[i].pos=shape.pos
            grey_placeholder_diamonds[i].pos=shape.pos
            grey_placeholder_circs[i].autoDraw=True
            grey_placeholder_diamonds[i].autoDraw=True
            
        wait_here(.5) # ################ Placeholders display (grey) ##################
        
        for greys in grey_placeholder_circs:
            greys.autoDraw=False
        for greys in grey_placeholder_diamonds:
            greys.autoDraw=False
        
        cue_circs=np.random.choice(stimuli,2, replace=False)
        dis_circ=cue_circs[0]
        tar_circ=cue_circs[1]
        
        target_stim.pos=tar_circ.pos
        tar_placeholder.pos=tar_circ.pos
        distractor_stim.pos=dis_circ.pos
        dis_placeholder.pos=dis_circ.pos
        target_stim.autoDraw=True
        distractor_stim.autoDraw=True
        dis_placeholder.autoDraw=True
        tar_placeholder.autoDraw=True
        for i in range(no_stim):
            shape=stimuli[i]
            if shape != tar_circ and shape!=dis_circ:
                #other_stim[i].pos=shape.pos
                other_stim[i].autoDraw=True
                other_placeholders[i].autoDraw=True
        
        fixation.autoDraw=True
        
        if EEGflag:
            thistrialFlag=cue_trigDict[thisBlock[trial][0]+'_'+SOA+'_cue_trig']
            win.callOnFlip(port.write,bytes([thistrialFlag]))
        
        SOA_num=SOA_maps[SOA]
        wait_here(SOA_num) # ############## Cue presentation ###################
        
        for o in other_placeholders: o.autoDraw=False
        for a in other_stim: a.autoDraw=False
        target_stim.autoDraw=False
        distractor_stim.autoDraw=False
        dis_placeholder.autoDraw=False
        tar_placeholder.autoDraw=False
        fixation.autoDraw=True
                
        distractor_stim.autoDraw=True
        target_stim.autoDraw=True
        for i in range(no_stim):
            shape=stimuli[i]
            if shape != tar_circ and shape!=dis_circ:
                #other_stim[i].pos=shape.pos
                other_stim[i].autoDraw=True
        
        bar_oris=np.random.permutation([0,0,0,0,90,90,90,90])
        for s in range(len(stimuli)):
            circs=stimuli[s]
            bars[s].pos=other_stim[s].pos #except target and distractor
            bars[s].ori=bar_oris[s]
            bars[s].autoDraw=True
            if circs==tar_circ:
                target_ori=bars[s].ori #then document the orientation of the bar at this loc
                print(target_ori)
        
        if target_ori==0:
            corrKey='q'#'up'
        elif target_ori==90:
            corrKey='p'#'left'

        
        if EEGflag:
                # port.flush()
                probetrig=probe_trigDict[thisBlock[trial][0]+'_'+SOA+'_probe_trig']
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
            subResp=event.getKeys(keyList=['q','p'], timeStamped=clock)
            win_count=win_count+1
            if win_count==max_win_count:
                break
        
        if not subResp:
            if EEGflag:
                port.write(bytes([other_trigDict['subNonRespTrig']]))
                resp_trig=other_trigDict['subRespTrig']
            
            trial_corr=np.nan
            RT=np.nan
            key='None'
        else:
            if EEGflag:
                port.write(bytes([other_trigDict['subRespTrig']]))
                resp_trig=other_trigDict['subRespTrig']
            if subResp[0][0]==corrKey:
                trial_corr=1
            else:
                trial_corr=0
                
            RT=subResp[0][1]
            key=subResp[0][0]
        
        fixation.draw()
        for shape in other_stim:
            shape.autoDraw=False
        for bar in bars:
            bar.autoDraw=False
        target_stim.autoDraw=False
        distractor_stim.autoDraw=False
        
        win.flip()
        #core.wait(ITI)
        
#        if trial_corr==0:
#            if expInfo['t.o. [y/n]']=='y':
#                timeout_msg.autoDraw=True
#                wait_here(1)
#                timeout_msg.autoDraw=False
#        
        if EEGflag:
            Thistrial_data= {'trialNum':(trial),'trial_type':thisBlock[trial][0],'SOA':SOA,'corrResp':corrKey,'subjectResp':key,'trialCorr?':trial_corr,'RT':RT,
                            'Tar,Dis,Other':(target_stim.name,distractor_stim.name,other_stim[0].name), 'tar,dis stim_loc':(tar_circ.name,dis_circ.name),'ITI':ITI,'trial_trigs':(thistrialFlag,probetrig,resp_trig)}
        else:
            Thistrial_data= {'trialNum':(trial),'trial_type':thisBlock[trial][0],'SOA':SOA,'corrResp':corrKey,'subjectResp':key,'trialCorr?':trial_corr,'RT':RT, 
                            'Tar,Dis,Other':(target_stim.name,distractor_stim.name,other_stim[0].name),'tar,dis stim_loc':(tar_circ.name,dis_circ.name),'ITI':ITI,'trial_trigs':'None'}
        trialDataList.append(Thistrial_data)
        
        print(Thistrial_data)
        
        key=event.getKeys()
        if key: 
            if key[0]=='escape': 
                win.close()
                core.quit()
                print('FORCED QUIT')
        
        if EEGflag:
            win.callOnFlip(port.write,bytes([other_trigDict['ITI_trig']]))
            
        #core.wait(ITI) #ITI--want to jitter this?, with an average of 4 seconds
        wait_here(ITI)
#            port.close()
#            
    
    blocks.update({'blockInfo_%i'%(block):{'block':blockNum,'trialsData':trialDataList}})
    
    # #########################saving data out###########################################
    if block==0:
        make_csv(filename,expStart=True)
    else:
        make_csv(filename,expStart=False)

if EEGflag:
    port.write(stopBlockflag)
#if EEGflag:
#    port.write(stopSaveflag)
#    port.close()

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