import mne
from mne.datasets import sample
from mne import io
from mne.preprocessing import create_ecg_epochs, create_eog_epochs
from mne.preprocessing import ICA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os 
from os import path
import pickle
import fnmatch
#import ipywidgets
#from ipywidgets import widgets


ROOT = '/home/dcellier/RDSS/AlphaStudy_Data/eegData/'
ROOT_raw=ROOT+'eeg_raw/'
ROOT_behav=ROOT+'eeg_behavior_data/'
ROOT_proc='/data/backed_up/shared/AlphaStudy_data/placeholders/preproc_EEG_matchingBrad/'
eyetrack_compiled_path='/data/backed_up/shared/AlphaStudy_data/placeholders/eyetracking_compiled_trials/'
subject_files=[]
subNum_list=['197','206','211','214','223',
             '224','225','226','228','233',
             '234','237','241','244','251',
             '247','240','231','254','264',
             '252','253','243','249','258',
             '257','248','255','245']
                #'193','196','198','204','212,'213','222','230','235','238','227','246','239''261',
        # sub 193 didn't have a full session
        # sub 196 should be processed, but doesn't have eyetracking calibration for now
        # sub 197 successfully preprocessed.
        # sub 198 unsure where eyetracking is, tried to process anyway but mismatch between behavior logs and bdf
        # sub 204 only has 531 events on bdf file, unusable
        # sub 206 successfully preprocessed
        # sub 211 preprocessed but missing ~ a block worth of eyetracking 
        # sub 212 had one more cue event than bdf. had to make a special behavioral csv for the cue epochs only
                    # But the missing cue event is a random one, not at beginning or end, so I have no idea
                    # which trial to cut out of behavioral log ughhhhh
        # sub 213 has missing events too, because of issue with PauseOn, unusable 
        # sub 214 missing triggers in eyetracking file, so preprocessed without eyetracking
        # sub 222 unusable line noise
        # sub 223 processed w eyetracking
        # sub 224 no eyetracking,processed without it.
                    # error re: shortest_event error? Manually fixed it like I did w thalhi (hardcoding)
                    # had to re-preprocess it because I realize the metadata was being incorrectly paired w each trial
        # sub 225 eyetracking ok, successfully processed
        # sub 226 processed
        # sub 227 only has four blocks because kept falling asleep. didn't process
        # sub 228 processed, but with one missing probe trial
        # sub 230 incomplete sub because some blocks were saved as behavioral
        # sub 231 preprocessed ok, w eyetracking. Probs don't analyze, not sure why it looks so weird
        # sub 233 processed ok, no eyetracking calibration
        # sub 234 processed ok w eyetracking
        # sub 235 power spectrum looks insane, going to skip this processing (probs also from motorized table)
        # sub 237 preprocessed ok 
        # sub 238 power spectrum looks insane here too, skipping. Power noise from the table (rukshads subject)
        # sub 239 session was cut short because he fell asleep, only did 3 blocks and didn't really do them. 
                    # Processed but shouldn't analyze
        # sub 240 eyetracking ok, preproc ok
        # sub 241 preproc ok
        # sub 243 no eyetracking,preproc ok
        # sub 244 preprocessed ok
        # sub 245 no eyetracking, preproc ok, missing 47 trials in block 2 
        # sub 246 no eyetrack calib file,
        # sub 247 preprocessed ok, had to set min_duration of events to the (2/512)
        # sub 248 eyetrack ok, preproc ok
        # sub 249 no eyetracking, min duration error at first
        # sub 251 had to set min duration to the (2/512)
        # sub 252
        # sub 253 no eyetracking, preproc without it
        # sub 254 no eyetracking, shortest event error, missing 2 probe trigs, preproc ok
        # sub 255 no eyetracking, preproc ok, 2 blocks of missing behav data
        # sub 257 no eyetracking, preproc ok
        # sub 261 no eyetracking, too many bdf events
        # sub 264 preproc ok, no eyetracking
        
        
for filename in os.listdir(ROOT_raw): #compiling the subjects downloaded from MIPDB
	for subNum in subNum_list:
		if subNum in filename:
			subject_files.append(filename)
            
s_file_copy=subject_files[:]
for thisSub in s_file_copy:
	sub_name=thisSub.split('_')[1]
	print(sub_name)
	if os.path.exists(ROOT_proc+sub_name+'/'):
		subject_files.remove(thisSub)
print(subject_files)
for sub in subject_files: # insert for loop through subject list here
	raw_file=ROOT_raw+sub
	sub_name=sub.split('_')[1]
	#print(sub_name)
	pattern=sub_name+'_alpha_placeholders_matchingBrad_*_*_*_*_*_*.csv'
	pattern2=sub_name+'_alpha_placeholders_matchingBrad_*_*_*_*_*.csv'
	pattern3=sub_name+'_alpha_placeholders_matchingBrad_*_*_*_*_*_TRUNCATED_TO_MATCH_BDF.csv'
	pattern4=sub_name+'_alpha_placeholders_matchingBrad_*_*_*_*_*_*_TRUNCATED_TO_MATCH_BDF.csv'
	behav_files=pd.DataFrame()
	for f in os.listdir(ROOT_behav):
		if fnmatch.fnmatch(f,pattern) or fnmatch.fnmatch(f,pattern2) or fnmatch.fnmatch(f,pattern3) or fnmatch.fnmatch(f,pattern4):
			print(f)
			behav_file=pd.read_csv(ROOT_behav+f,engine='python')
			behav_files=behav_files.append(behav_file,ignore_index=True)
	behav_files=behav_files.sort_values(['block','trialNum']).reset_index() # adding so that pandas imports trials and blocks in order
	#behav_files.dropna(axis=0,inplace=True,how='any')
	#behav_files.to_csv('/home/dcellier/RDSS/AlphaStudy_Data/eegData/eeg_behavior_data/compiledAllBlocks_fromPreprocScript_s233_before_eyes.csv')   
	if not os.path.exists(eyetrack_compiled_path+'sub_'+sub_name+'_trialsCompiled.csv'):
		## check to see if there's an edited version of the eyetracking
		if os.path.exists(eyetrack_compiled_path+'sub_'+sub_name+'_trialsCompiled_TRUNCATED_TO_MATCH.csv'):
			eyes=pd.read_csv(eyetrack_compiled_path+'sub_'+sub_name+'_trialsCompiled_TRUNCATED_TO_MATCH.csv')
			behav_files=pd.concat([behav_files,eyes],ignore_index=False,axis=1) 
		else:    
			continue_noEye=input('This subject does not have an eyetracking compiled trials csv on record. Continute anyway? [y/n] ')
			if continue_noEye=='n':
				exit()
			elif continue_noEye !='y':
				print('oops, please specify [y/n]')
				exit()
	else:            
		eyes=pd.read_csv(eyetrack_compiled_path+'sub_'+sub_name+'_trialsCompiled.csv')
		behav_files=pd.concat([behav_files,eyes],ignore_index=False,axis=1)
	behav_files.to_csv('/home/dcellier/RDSS/AlphaStudy_Data/eegData/eeg_behavior_data/compiledAllBlocks_fromPreprocScript_s243.csv')       
	print(behav_files)
	if sub_name in ['261','245']:
		raw=mne.io.read_raw_fif(raw_file,preload=True)
	else:
		raw=mne.io.read_raw_edf(raw_file,montage=mne.channels.read_montage('biosemi64'),preload=True)
	#raw.plot(n_channels=72)

	# # Re-reference, apply high and low pass filters (1 and 50) # # # # # # # # # #

	raw_f=raw.copy()
	raw_f.filter(1,50)
	raw_f.set_channel_types({'EXG1':'emg','EXG2':'emg','EXG3':'eog','EXG4':'eog','EXG5':'eog','EXG6':'eog',
                        'EXG7':'ecg','EXG8':'emg'})
	
	#raw_f.plot(n_channels=72)
	raw_f.plot_psd()
	
		# # # # # # selecting bad electrodes # # # # # #	
	raw_fi=raw_f.copy()	
	raw_DataCH=(raw_fi.copy()).drop_channels(['EXG1', 'EXG2','EXG3','EXG4','EXG5','EXG6','EXG7','EXG8'])
	tryAgain=1
	while tryAgain:
		raw_DataCH.plot(block=True) #pauses script while i visually inspect data and select which channels to delete
		bads=raw_DataCH.info['bads']
		text_msg2=input('The channels you marked as bad are: '+str(bads)+' \n Are you ready to interpolate? [y/n]: ')
		if text_msg2=='y':
			raw_fi.info['bads']=bads
			raw_fi=raw_fi.interpolate_bads()
			tryAgain=0
		elif text_msg2=='n':
			tryAgain=1	
		else:
			print('invalid entry: '+text_msg2)
			tryAgain=1
	raw_fir,r= mne.set_eeg_reference(raw_fi,ref_channels=['EXG1', 'EXG2'])#,'EXG8'])#mastoids, nose -- nose we decided we didn't want to use to reref


	# # Finding Events (triggers) # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	if sub_name in ['224','247','251','249','254']:
		events=mne.find_events(raw_fir,verbose=True,min_duration=(2/512))
	else:
		events = mne.find_events(raw_fir, verbose=True)

	raw_fe=raw_fir.copy() # raw_fe was originally the 2 epoched data
	#raw_fe.plot()
	
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
	    
	epCond={}
	print('\n\n\n Epoching Conds \n ')
    
	if sub_name=='212':
		epCond['cue_events']=mne.Epochs(raw_fe, events=events, baseline=baseline, event_id=cue_event_id, tmin=cue_tmin,tmax=cue_tmax,metadata=pd.read_csv('/data/backed_up/shared/AlphaStudy_data/placeholders/eyetracking_compiled_trials/sub_212_trialsCompiled_wBehav_data_FOR_CUES.csv')) 
        #special csv with one trial cut off bc the pauseon flag was tripped right before the last cue trig it looks like?
	else:
		epCond['cue_events']=mne.Epochs(raw_fe, events=events, baseline=baseline, event_id=cue_event_id, tmin=cue_tmin,tmax=cue_tmax,metadata=behav_files)
        
	if sub_name=='228': # hard coding this bc one trig is missing from one trial for probes only
		epCond['probe events']=mne.Epochs(raw_fe, events=events, baseline=(2,5.4), event_id=probe_event_id, tmin=probe_tmin, tmax=probe_tmax,metadata=pd.read_csv('/data/backed_up/shared/AlphaStudy_data/placeholders/eyetracking_compiled_trials/sub_228_trialsCompiled_wBehav_data_FOR_PROBE.csv'))
	elif sub_name=='254': # hard coding this bc one trig is missing from one trial for probes only
		epCond['probe events']=mne.Epochs(raw_fe, events=events, baseline=(2,5.4), event_id=probe_event_id, tmin=probe_tmin, tmax=probe_tmax,metadata=pd.read_csv('/home/dcellier/RDSS/AlphaStudy_Data/eegData/eeg_behavior_data/sub254_TRUNCATED_TO_MATCH_probeOnly.csv'))
	else:
		epCond['probe events']=mne.Epochs(raw_fe, events=events, baseline=(2,5.4), event_id=probe_event_id, tmin=probe_tmin, tmax=probe_tmax,metadata=behav_files)
     # baseline correcting to the ITI

	# # Inspect and reject bad epochs # # # # # # # # # # # #  # # # # # # # # # # 
	# # AND ICA on Raw data # # # # # # # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # # # # # 
	our_picks=mne.pick_types(raw_fe.info,meg=False,eeg=True,eog=False)#mne.pick_types(raw_fi.info,meg=False,eeg=True,eog=True,emg=True,stim=True,ecg=True)
 
	layout=mne.channels.read_montage('biosemi64')

	EOG_channels=['EXG3', 'EXG4', 'EXG5', 'EXG6']
	ECG_channels=['EXG7']

	for ev in epCond.keys():
		plotEpoch=1
		while plotEpoch:
			print('plotting ' +ev)
			keep_plotting=1
			while keep_plotting:
				thisEp=[]
				thisEp=epCond[ev].copy()
				thisEp.load_data()
				print(thisEp)
				thisEp.plot(block=True, title="SELECT BAD EPOCHS: "+ev, n_epochs=6,n_channels=15)
				bads=input('Are you sure you want to continue? [y/n]: ')
				if bads=='y':
					#epCond[ev]=thisEp
					keep_plotting=0
				elif bads=='n':
					continue
				else:
					print('oops, please indicate which epochs you would like to reject')
			### ICA ###
			thisCond=thisEp.copy()
			thisCond.set_montage(layout)
			ica=ICA(n_components=64,random_state=25)
			ica.fit(thisCond,picks=our_picks)
			eog_ic=[]
			for ch in EOG_channels:
				#find IC's attributable to EOG artifacts
				eog_idx,scores=ica.find_bads_eog(thisCond,ch_name=ch)
				eog_ic.append(eog_idx)
			ecg_ic=[]
			for ch in ECG_channels: # find IC's attributable to ECG artifacts
				ecg_idx,scores=ica.find_bads_ecg(thisCond,ch_name=ch)
				ecg_ic.append(ecg_idx)
			reject_ic=[]
			for eog_inds in eog_ic:
				for ele in eog_inds:
					if (ele not in reject_ic) and (ele <= 31):
						reject_ic.append(ele)
			for ecg_inds in ecg_ic:
				for ele in ecg_inds:
					if (ele not in reject_ic) and (ele <= 31):
						reject_ic.append(ele) #add these IC indices to the list of IC's to reject
			ica.exclude=[]
			ica.exclude.extend(reject_ic)
			plotICA=1
			while plotICA:
				ica.plot_components(picks=range(32),ch_type=None,cmap='interactive',inst=thisCond)# changed to ch_type=None from ch_type='EEG'because this yielded an error
				#ica.plot_components(picks=range(32,64),ch_type=None,cmap='interactive',inst=thisCond)
				input('The ICs marked for exclusion are: '+str(ica.exclude)+ '\n Press enter.')
				thisCond.load_data()
				thisCond.copy().plot(title=ev+': BEFORE ICA',n_epochs=5,n_channels=30)
				thisCond_copy=thisCond.copy()
				thisCond_Ic=ica.apply(thisCond_copy,exclude=ica.exclude)
				thisCond_Ic.plot(block=True, title=ev+': AFTER ICA',n_epochs=5,n_channels=30)
				verification_ic=input('The ICs marked for rejection are: ' + str(ica.exclude) +'\n Are you sure you want to proceed? [y/n]: ')
				if verification_ic=='y':
					plotICA=0
				else:
					print('Please select which ICs you would like to reject')
			save_ep=input('Save this epoch? Entering "no" will take you back to epoch rejection for this condition. [y/n]: ')
			if save_ep=='y':
				plotEpoch=0
		#ica.plot_components(picks=range(25),ch_type=None,inst=thisEp)  
		thisCond_copy=thisCond.copy()
		ica.apply(thisCond_copy)
		thisCond_copy.drop_channels(['EXG1', 'EXG2','EXG3','EXG4','EXG5','EXG6','EXG7','EXG8'])		
		epCond[ev]=thisCond_copy
	
	print('\n\n\n\n SAVING OUT INFO ~~~~~~~ \n\n')
	save_path=ROOT_proc+sub_name+'/'
	os.mkdir(save_path)

	
	for event in epCond.keys():
		event_name=event.split('_')[0]
		thisEp=epCond[event]
		thisEp.save(save_path+event_name+'-epo.fif')
		os.chmod(save_path+event_name+'-epo.fif',0o660)
	os.chmod(save_path,0o2770)
	ask=1
	exit_loop=0
	while ask:	
		end_msg=input('Continue on to next sub? [y/n]')
		if end_msg=='y':
			ask=0
		elif end_msg=='n':
			exit_loop=1
			ask=0
		else:
			print('Oops! Please answer y/n')

	if exit_loop:
		break