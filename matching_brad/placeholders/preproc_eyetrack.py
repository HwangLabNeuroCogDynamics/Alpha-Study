import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

eyetrack_out_path='/data/backed_up/shared/AlphaStudy_data/placeholders/eyetracking_compiled_trials/'
eyetrack_in_path='/home/dcellier/RDSS/AlphaStudy_Data/eegData/eeg_eyetracking/'

eyetracking_files=os.listdir(eyetrack_in_path)
#print(eyetracking_files)
subs=[]
for f in eyetracking_files:
    if ('calibration') in f or ('testing' in f):
        sub_num=f.split('_')[1]
        subs.append(sub_num)
    subs=list(np.unique(subs))
print(subs)
print('SUBJECTS THAT ARE ALREADY PROCESSED: \n')
for f in os.listdir(eyetrack_out_path):
    subs_copy=subs[:]
    for s in subs_copy:
        if s in f:
            print(s)
            subs.remove(s)
    
print(subs)


## plotting the calibrations so that I can have a point of reference for the scale of the testing file
def plot_calibrations(sub_num,eyetracking_files=eyetracking_files):
    
    subs_calibrations=[f for f in eyetracking_files if ((sub_num in f) and ('calibration' in f) and ('meta' not in f))]
    
    print("\nPLOTTING CALIBRATION")
    for calib_f in subs_calibrations: # there may be multiple calibration files for multiple blocks
        print(calib_f)
        calib=pd.read_csv(eyetrack_in_path+calib_f)
        if len(calib[np.uint8(calib[' Trigger']) !=0])==0: 
            # if the calibration file doesn't contain any triggers (oldest files won't)
            # then we just plot all of the points we have
            x=calib[' LeftScreenX']
            y=calib[' LeftScreenY']
            a=calib[' RightScreenX']
            b=calib[' RightScreenY']
            plt.plot(x,y)
            plt.plot(a,b)
            plt.show()
        else:
            # plot all of the time points from the first triggers to the last ones
            all_trigs=calib[np.uint8(calib[' Trigger']) != 0]
            all_trigs[' Trigger']=np.uint8(all_trigs[' Trigger'])
            
            if (167 in list(all_trigs[' Trigger'])) or (169 in list(all_trigs[' Trigger'])): 
                # these are the triggers that mark the beginning and the end of the circles being presented
                # but, not all of the older files have it
                begin_trigs=all_trigs[all_trigs[' Trigger']==167]['Timestamp'].iloc[0]
                end_trigs=all_trigs[all_trigs[' Trigger']==169]['Timestamp'].iloc[0] 
            else:
                begin_trigs=all_trigs['Timestamp'].iloc[0]
                end_trigs=all_trigs[all_trigs[' Trigger']==165]['Timestamp'].iloc[-1]
                # end_trigs will be when the last circle appears, 
                # but we want to expand that past just the trigger by 4 seconds
                # Since the sampling rate of the eyetracker is 500 Hz, this means we add on approximately
                # 1,000,000 * 4 time points to get to the 'end' of the trigger
                end_trigs=end_trigs+4000000
            
            between_trigs=calib[calib['Timestamp'] > begin_trigs][calib['Timestamp'] < end_trigs]
            x=between_trigs[' LeftScreenX']
            y=between_trigs[' LeftScreenY']
            a=between_trigs[' RightScreenX']
            b=between_trigs[' RightScreenY']
            plt.plot(x,y)
            plt.plot(a,b)
            plt.show()
            
        Ok_to_continue=input('Move on from this calibration? [1/0]')
        #print(type(Ok_to_continue))
        if Ok_to_continue:
            continue
        else:
            exit()

## Sort_trials loops through each line of the testing eyetracker file and sorts into suspected trials based on the order of the triggers found (should be in order of mask, then cue, then probe triggers, then ITI
    ## outputs three dataframes, one for each stage of trial (mask,cue,probe)
    
def sort_trials(df):
    example2=df
    
    cue_epochs=pd.DataFrame()
    probe_epochs=pd.DataFrame()
    mask_epochs=pd.DataFrame()
    
    cue_trigs=[101,103,105,107,109,111]
    probe_trigs=[113,115,117,119,121,123]
    mask_trig=125
    ITI_trig=127

    n=0
    trial_num=-1
    while n < len(example2):
        thisRow=example2.iloc[n] # loop through each row
        thisTrig=thisRow[' Trigger']
        if thisTrig != 0: #until you find a trigger that is something other than zero
                            # then loop thru these rows until you've collected the whole trial
            if thisTrig == mask_trig: # the mask trigger marks the beginning of a trial
                trial_num=trial_num+1
                #start_time=thisRow['Timestamp'] # record the timestamp where this began
                nextTrig=0 # just to initialize the variable
                trial_trig_mask=example2.iloc[n][' Trigger']
                while nextTrig not in cue_trigs: # loop thru rows until you hit the next stage of the trial
                    thisRow=example2.iloc[n]
                    thisTime=thisRow['Timestamp']
                    thisTrig=thisRow[' Trigger']
                    leftX=thisRow[' LeftScreenX']
                    leftY=thisRow[' LeftScreenY']
                    rightX=thisRow[' RightScreenX']
                    rightY=thisRow[' RightScreenY']
                    mask_ep={'Timestamp':thisTime,'Trigger':trial_trig_mask,'Trial':trial_num,
                             'leftX': leftX, 'leftY':leftY,'rightX':rightX,'rightY':rightY}
                    mask_epochs=mask_epochs.append(mask_ep,ignore_index=True)                
                    nextTrig=example2.iloc[n+1][' Trigger']
                    n+=1
                # if nextTrig is equal to one of the cue period triggers, this while loop will stop
                # and trigger the next while loop to document the cue epochs, until it finds a probe trig
                trial_trig_cue=example2.iloc[n][' Trigger']
                while nextTrig not in probe_trigs:
                    thisRow=example2.iloc[n]
                    thisTime=thisRow['Timestamp']
                    thisTrig=thisRow[' Trigger']
                    leftX=thisRow[' LeftScreenX']
                    leftY=thisRow[' LeftScreenY']
                    rightX=thisRow[' RightScreenX']
                    rightY=thisRow[' RightScreenY']
                    cue_ep={'Timestamp':thisTime,'Trigger':trial_trig_cue,'Trial':trial_num,
                            'leftX': leftX, 'leftY':leftY,'rightX':rightX,'rightY':rightY}
                    cue_epochs=cue_epochs.append(cue_ep,ignore_index=True)                
                    nextTrig=example2.iloc[n+1][' Trigger']
                    n+=1  
                trial_trig_probe=example2.iloc[n][' Trigger']
                while (nextTrig != ITI_trig) and ((example2.iloc[n][' Trigger'] in probe_trigs) or (example2.iloc[n][' Trigger']==0)):
                    thisRow=example2.iloc[n]
                    thisTime=thisRow['Timestamp']
                    thisTrig=thisRow[' Trigger']
                    leftX=thisRow[' LeftScreenX']
                    leftY=thisRow[' LeftScreenY']
                    rightX=thisRow[' RightScreenX']
                    rightY=thisRow[' RightScreenY']
                    probe_ep={'Timestamp':thisTime,'Trigger':trial_trig_probe,'Trial':trial_num,
                              'leftX': leftX, 'leftY':leftY,'rightX':rightX,'rightY':rightY}
                    probe_epochs=probe_epochs.append(probe_ep,ignore_index=True)                
                    nextTrig=example2.iloc[n+1][' Trigger']
                    n+=1  
                print(trial_num)
                print(trial_trig_mask,trial_trig_cue,trial_trig_probe)
                # when this trial is over with, we can exit the loop and keep going through 
                # rows until we hit another mask epoch


        n+=1
    return cue_epochs,probe_epochs,mask_epochs
    
    
## Compile_trials uses the outputs of sort_trials and organizes it such that it may be appended to the behavioral log of the subject and ultimately appended to the bdf file during eeg preprocessing. 
    ## output is one dataframe where each row is one trial and the columns are the x and y values (lists)
    ## for the eyetracking data for each part of that trial
    
def compile_trials(cue_epochs,probe_epochs,mask_epochs,expected_trials=600):
    
    compiled_trials=pd.DataFrame()
    
    #checking if all of the expected trials are there
    if not np.max(mask_epochs['Trial'])==expected_trials-1:
        print("WARNING: not all expected trials were found during the indexing of the eyetracking file")
        
    if np.max(mask_epochs['Trial'])==np.max(probe_epochs['Trial'])==np.max(cue_epochs['Trial']):
        trialN=np.max(mask_epochs['Trial'])
        print(trialN)
        for n in range(int(trialN)+1):
            thisTrialdat_m=mask_epochs[mask_epochs['Trial']==n]
            trigger_m=thisTrialdat_m['Trigger'].iloc[0]
            theseXs_left_m=list(thisTrialdat_m['leftX'])
            theseYs_left_m=list(thisTrialdat_m['leftY'])
            theseXs_right_m=list(thisTrialdat_m['rightX'])
            theseYs_right_m=list(thisTrialdat_m['rightY'])
            startTrialTime_m=thisTrialdat_m['Timestamp'].iloc[0]
            stopTrialTime_m=thisTrialdat_m['Timestamp'].iloc[-1]

            thisTrialdat_c=cue_epochs[cue_epochs['Trial']==n]
            trigger_c=thisTrialdat_c['Trigger'].iloc[0]
            theseXs_left_c=list(thisTrialdat_c['leftX'])
            theseYs_left_c=list(thisTrialdat_c['leftY'])
            theseXs_right_c=list(thisTrialdat_c['rightX'])
            theseYs_right_c=list(thisTrialdat_c['rightY'])
            startTrialTime_c=thisTrialdat_c['Timestamp'].iloc[0]
            stopTrialTime_c=thisTrialdat_c['Timestamp'].iloc[-1]

            thisTrialdat_p=probe_epochs[probe_epochs['Trial']==n]
            trigger_p=thisTrialdat_p['Trigger'].iloc[0]
            theseXs_left_p=list(thisTrialdat_p['leftX'])
            theseYs_left_p=list(thisTrialdat_p['leftY'])
            theseXs_right_p=list(thisTrialdat_p['rightX'])
            theseYs_right_p=list(thisTrialdat_p['rightY'])
            startTrialTime_p=thisTrialdat_p['Timestamp'].iloc[0]
            stopTrialTime_p=thisTrialdat_p['Timestamp'].iloc[-1]



            compiled_trials_row={'Eyetrack_trial':n,
                                 
                                 'TrialTrigs(m,c,p)':(trigger_m,trigger_c,trigger_p),

                                 'Timestamp_start_mask':startTrialTime_m,
                                 'Timestamp_stop_mask':stopTrialTime_m,'leftX_mask':theseXs_left_m,
                                 'leftY_mask':theseYs_left_m,'rightX_mask':theseXs_right_m,
                                 'rightY_mask':theseYs_right_m,

                                 'Timestamp_start_cue':startTrialTime_c,
                                 'Timestamp_stop_cue':stopTrialTime_c,'leftX_cue':theseXs_left_c,
                                 'leftY_cue':theseYs_left_c,'rightX_cue':theseXs_right_c,
                                 'rightY_cue':theseYs_right_c,

                                 'Timestamp_start_probe':startTrialTime_p,
                                 'Timestamp_stop_probe':stopTrialTime_p,'leftX_probe':theseXs_left_p,
                                 'leftY_probe':theseYs_left_p,'rightX_probe':theseXs_right_p,
                                 'rightY_probe':theseYs_right_p

                                }
            compiled_trials=compiled_trials.append(compiled_trials_row,ignore_index=True)
    else:
        print("CONDITIONS MUST MATCH IN TERMS OF NUMBER OF TRIALS")
        exit()

    return compiled_trials

def continue_msg():
    ask_continue_msg=input("Continue to saving out? [1/0]")
    if not ask_continue_msg:
        exit()
    elif ask_continue_msg not in ['1','0']:
        print("oops, please enter 1/0")
        continue_msg()
    elif ask_continue_msg:
        print('Compiling trials, saving out')

for sub in subs:
    if sub not in ['198','214','196','224','230']: # excluding this subject for now because the calibration file is corrupt
        if sub not in ['196','233']: # sub196 doesn't have a functioning calibration file, but want to process anyway
            plot_calibrations(sub_num=sub)
            
        # some subs have more than one file bc we re-calibrated in the middle of it
        thisSubs_files=[]
        for file in eyetracking_files:
            if (sub in file) and ('testing' in file) and ('meta' not in file):
                thisSubs_files.append(file)
                
        if len(thisSubs_files) ==1:
            for file in eyetracking_files:
                if (sub in file) and ('testing' in file) and ('meta' not in file):

                    print("LOADING FILE FOR SUB {0}".format(sub))
                    testing_log=pd.read_csv(eyetrack_in_path+file)
                    # converting series to match our triggers (bytes)
                    testing_log[' Trigger']=np.uint8(testing_log[' Trigger']) 

                    print("\n\nSorting eyetracking file into trials, please be patient....")
                    cue_eps,probe_eps,mask_eps= sort_trials(testing_log)

                    #plotting the results of the cue_eps                
                    a=cue_eps['leftX']
                    b=cue_eps['leftY']
                    x=cue_eps['rightX']
                    y=cue_eps['rightY']
                    plt.plot(x,y, '.-')
                    plt.plot(a,b, '-.')
                    plt.title('Cue Epochs')
                    plt.show()

                    #plotting the results of the probe_eps                
                    a=probe_eps['leftX']
                    b=probe_eps['leftY']
                    x=probe_eps['rightX']
                    y=probe_eps['rightY']
                    plt.plot(x,y, '.-')
                    plt.plot(a,b, '-.')
                    plt.title('Probe Epochs')
                    plt.show()

                    #plotting the results of the mask_eps                
                    a=mask_eps['leftX']
                    b=mask_eps['leftY']
                    x=mask_eps['rightX']
                    y=mask_eps['rightY']
                    plt.plot(x,y, '.-')
                    plt.plot(a,b, '-.')
                    plt.title('Mask Epochs')
                    plt.show()

                    continue_msg()                    

                    out_df=compile_trials(cue_epochs=cue_eps,probe_epochs=probe_eps,mask_epochs=mask_eps,expected_trials=600)

                    out_df.to_csv(eyetrack_out_path+'sub_'+sub+'_trialsCompiled.csv')

        elif len(thisSubs_files) >1:
            testing_log=pd.Dataframe()
            for file in thisSubs_files:
                print( "\n COMPILING MULTIPLE FILES")
                one_file=pd.read_csv(eyetrack_in_path+file)
                testing_log=testing_log.append(one_file,ignore_index=True)
            
            # converting series to match our triggers (bytes)
            testing_log[' Trigger']=np.uint8(testing_log[' Trigger']) 

            print("\n\nSorting eyetracking file into trials, please be patient....")
            cue_eps,probe_eps,mask_eps= sort_trials(testing_log)

            #plotting the results of the cue_eps                
            a=cue_eps['leftX']
            b=cue_eps['leftY']
            x=cue_eps['rightX']
            y=cue_eps['rightY']
            plt.plot(x,y, '.-')
            plt.plot(a,b, '-.')
            plt.title('Cue Epochs')
            plt.show()

            #plotting the results of the probe_eps                
            a=probe_eps['leftX']
            b=probe_eps['leftY']
            x=probe_eps['rightX']
            y=probe_eps['rightY']
            plt.plot(x,y, '.-')
            plt.plot(a,b, '-.')
            plt.title('Probe Epochs')
            plt.show()

            #plotting the results of the mask_eps                
            a=mask_eps['leftX']
            b=mask_eps['leftY']
            x=mask_eps['rightX']
            y=mask_eps['rightY']
            plt.plot(x,y, '.-')
            plt.plot(a,b, '-.')
            plt.title('Mask Epochs')
            plt.show()

            continue_msg()                    
                
            out_df=compile_trials(cue_epochs=cue_eps,probe_epochs=probe_eps,mask_epochs=mask_eps,expected_trials=600)

            out_df.to_csv(eyetrack_out_path+'sub_'+sub+'_trialsCompiled.csv')    
                
                
                
                