import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import mne

ROOT_preproc='/data/backed_up/shared/AlphaStudy_data/placeholders/preproc_EEG_matchingBrad/'
ROOT_out='/data/backed_up/shared/AlphaStudy_data/placeholders/preproc_EEG_matchingBrad_removingNonFixationTrials/'
list_subs=os.listdir(ROOT_preproc)

preproc_cue_eps={}
preproc_probe_eps={}
for s in list_subs:
    if (s !="245") and (s not in os.listdir(ROOT_out)):
        cue=mne.read_epochs(ROOT_preproc+s+'/'+'cue-epo.fif')
        #probe=mne.read_epochs(ROOT_preproc+s+'/'+'probe events-epo.fif')
        preproc_cue_eps[s]=cue
        #preproc_probe_eps[s]=probe
        

ROOT = '/home/dcellier/RDSS/AlphaStudy_Data/eegData/'
ROOT_raw=ROOT+'eeg_raw/'
unproc_cues={}
unproc_probes={}

for sub_name in preproc_cue_eps.keys():
    
    print('\nLOADING RAW FILE  FOR: '+sub_name+'\n')
    for bdfFile in os.listdir(ROOT_raw):
        if sub_name in bdfFile:
            raw_file=ROOT_raw+bdfFile

    if sub_name in ['261','245']:
        raw=mne.io.read_raw_fif(raw_file,preload=True)
    else:
        raw=mne.io.read_raw_bdf(raw_file,montage=mne.channels.read_montage('biosemi64'),preload=True)
        
    print(raw.info['ch_names'])
        
    ch_type_dict={"EXG1":'eog',"EXG2":'eog',"EXG3":'eog','EXG4':'eog',"Status":'stim'}
    otherChs={ch:'eeg' for ch in raw.info['ch_names'] if ch not in list(ch_type_dict.keys())}
    ch_type_dict.update(otherChs)
    
    raw.set_channel_types(ch_type_dict)
        

        # # Finding Events (triggers) # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if sub_name in ['224','247','251','249','254']:
        events=mne.find_events(raw,verbose=True,min_duration=(2/512))
    else:
        events = mne.find_events(raw, verbose=True)

    # # Looping through conditions, epoching # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # # #

    #    startSaveflag=bytes([201])
    #    stopSaveflag=bytes([255])
    #    cue_trigDict={'dis_short_cue_trig': 101,
    #                 'dis_long_cue_trig':103,
    #                'tar_short_cue_trig':105,
    #               'tar_long_cue_trig':107,
    #              'neut_short_cue_trig':109,
     #             'neut_long_cue_trig':111}

    #    probe_trigDict={'dis_short_probe_trig': 113,
    #                 'dis_long_probe_trig':115,
    #                'tar_short_probe_trig':117,
    #               'tar_long_probe_trig':119,
    #              'neut_short_probe_trig':121,
     #             'neut_long_probe_trig':123}

    #    other_trigDict={'grey_placeholders_trig':125, 'ITI_trig':127,'subNonRespTrig':129,'subRespTrig':131}

    probe_event_id={'disShortProbe_trig':113,'disLongProbe_trig':115,'tarShortProbe_trig':117,
                    'tarLongProbe_trig':119,'neutShortProbe_trig':121,'neutLongProbe_trig':123}   
    #response_event_id={'subResp_trig':131,'subNonResp_trig':129}
    cue_event_id={'disShortCue_trig':101,'disLongCue_trig':103,'tarShortCue_trig':105,
                 'tarLongCue_trig':107,'neutShortCue_trig':109, 'neutLongCue_trig':111}

    cue_tmin, cue_tmax = -1.3,1 #-800 ms for baseline,plus grey placeholders 500ms long, then 100ms or 1000ms for cue time
    probe_tmin, probe_tmax = 0,5.4 # 2 second probe/response period + min ITI 3400ms
    #response_tmin,response_tmax=-0.5,1.5 # probably won't analyze this but might as well have it
    baseline = (None, -0.3) #baseline correction applied with mne.Epochs, this is starting @ beginning of epoch ie -0.8 

    print('\n\n\n Epoching Conds \n ')
    
        
    #eog_evs=mne.preprocessing.find_eog_events(raw,event_id=998)#,ch_name='EXG1')
    #eog_eps=mne.preprocessing.create_eog_epochs(raw,event_id=998)
    #eog_eps.plot(block=True)
    #onsets = eog_evs[:, 0] / raw.info['sfreq'] - 0.25
    #durations = [0.5] * len(eog_evs)
    #descriptions = ['bad blink'] * len(eog_evs)
    #blink_annot = mne.Annotations(onsets, durations, descriptions,
     #                             orig_time=raw.info['meas_date'])
    #raw.set_annotations(blink_annot)
    #raw.plot(events=eog_evs,block=True)
    

    unproc_cues[sub_name]=mne.Epochs(raw, events=events, baseline=baseline, event_id=cue_event_id, tmin=cue_tmin,tmax=cue_tmax,reject_by_annotation=True)
    unproc_probes[sub_name]=mne.Epochs(raw, events=events, baseline=(2,5.4), event_id=probe_event_id,tmin=probe_tmin, tmax=probe_tmax,reject_by_annotation=True)
    
    
for sub_name in preproc_cue_eps.keys():
    
    print("\nLOADING SUB "+sub_name+'\n')

    thisSub_dropLog=preproc_cue_eps[sub_name].drop_log
    thisSub_bool_vals=[]

    for ev in thisSub_dropLog:
        if ev==[]: # if the epoch is represented by an empty list 
                   # this means it still remains in the preproc epochs obj
            thisSub_bool_vals.append(False)
        elif ev==['USER']:
            thisSub_bool_vals.append(True)

    assert len(thisSub_bool_vals)==len(unproc_cues[sub_name].events)
    
    unproc_cues_matchingEps=unproc_cues[sub_name].copy().drop(thisSub_bool_vals) 
        #generating a ver with dropped epochs
        
    print(len(unproc_cues_matchingEps.events))
    assert len(unproc_cues_matchingEps.events) == len(preproc_cue_eps[sub_name].events)
    assert unproc_cues_matchingEps.drop_log == thisSub_dropLog
        # making sure it's the right # of events
        # and has a matching drop log
        # before replacing this item in the unproc_cues dictionary

    #unproc_cues[sub_name]=unproc_cues_matchingEps
    unproc_EXG_chs=unproc_cues_matchingEps.load_data().pick_channels(ch_names=['EXG1','EXG2','EXG3','EXG4'])
    preproc_cue_eps[sub_name]=preproc_cue_eps[sub_name].add_channels(
        add_list=[unproc_EXG_chs],force_update_info=True)

#preproc_cue_eps['253'].load_data().plot(show=True,block=True,picks=['EXG1','EXG2','EXG3','EXG4'])

print(preproc_cue_eps['253'].info['ch_names'][68:])


for sub in preproc_cue_eps.keys():
    print(sub)
    dist_of_epochs=[]
    NEps=len(preproc_cue_eps[sub])
    for ep in preproc_cue_eps[sub]:
        ep_EOG_data_ch3=ep[67,:]
        ep_EOG_data_ch4=ep[68,:]
        print(ep.shape)
        print(np.max(ep_EOG_data_ch3)-np.min(ep_EOG_data_ch3))
        rangeCh3=np.max(ep_EOG_data_ch3)-abs(np.min(ep_EOG_data_ch3))
        rangeCh4=np.max(ep_EOG_data_ch4)-abs(np.min(ep_EOG_data_ch4))
        if rangeCh3 > rangeCh4:
            maxRange=rangeCh3
        else:
            maxRange=rangeCh4
        dist_of_epochs.append(maxRange)
    third=(np.max(dist_of_epochs)-np.min(dist_of_epochs))/4
    minPlusThird=np.min(dist_of_epochs)+third
    fig,ax=plt.subplots()
    x=np.asarray(range(1,NEps+1))
    y=np.asarray(dist_of_epochs)
    print("\n\nPLOTTING SUB {0}".format(sub))
    plt.plot(x,y)
    #plt.scatter(x,y)
    plt.plot(x,np.asarray([minPlusThird]*NEps))
    for i,label in enumerate(x):
        ax.annotate(label, (x[i],y[i]))
#    plt.show()
                
    
#    for epIndex in range(len(preproc_cue_eps[sub])):
 #       thisEpDat=preproc_cue_eps[sub][epIndex]
  #      thisEpEOG=ep_EOG_data=thisEpDat[68:,:]
   #     thisEpMax=np.max(thisEpMax)
        
        
    thisSubCopy=preproc_cue_eps[sub].load_data().copy()
    thisSubCopy.plot(show=True,block=True,picks=['EXG1','EXG2','EXG3','EXG4'])
    if not os.path.exists(ROOT_out+sub+'/'):
        os.mkdir(ROOT_out+sub+'/')
    thisSubCopy.save(ROOT_out+sub+'/'+'cue_enforcedFix-epo.fif')
    
    
    
    
