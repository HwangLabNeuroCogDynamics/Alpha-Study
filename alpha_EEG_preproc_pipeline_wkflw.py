# # this is the EEG preproc wkflow to be used with alpha study EEG # #

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


#import kai's test data
ROOT = '/home/dcellier/RDSS/AlphaStudy_Data/eegData/'
ROOT_raw=ROOT+'eeg_raw/'
ROOT_behav=ROOT+'eeg_behavior_data/'
ROOT_proc='/data/backed_up/shared/AlphaStudy_data/EEG_preprocessed/'
subject_files=[]
for filename in ['Klaudiatest_03-07-19.bdf']:#os.listdir(ROOT_raw): #compiling the subjects downloaded from MIPDB
	if not filename=='realpeople':
		subject_files.append(filename)
for thisSub in subject_files:
	sub_name=thisSub.split('_')[0]
	if os.path.exists(ROOT_proc+sub_name+'/'):
		subject_files.remove(thisSub)
print(subject_files)
for sub in subject_files: # insert for loop through subject list here
	raw_file=ROOT_raw+sub
	sub_name=sub.split('_')[0]
	pattern='klaudiatest1_alpha_pilot_01_2019_Mar_07_1442.csv'#sub+'_alpha_pilot_01_20*_*_*_*.csv'
	for f in os.listdir(ROOT_behav):
		if fnmatch.fnmatch(f,pattern):
			sub_behav=f
	behav_file=pd.read_csv(ROOT_behav+sub_behav,engine='python')
	raw=mne.io.read_raw_edf(raw_file,montage=mne.channels.read_montage('biosemi64'),preload=True)
	#raw.plot(n_channels=72)

	# # Re-reference, apply high and low pass filters (1 and 50) # # # # # # # # # #

	raw_f=raw.copy()
	raw_f.filter(1,50)
	raw_f.set_channel_types({'EXG1':'emg','EXG2':'emg','EXG3':'eog','EXG4':'eog','EXG5':'eog','EXG6':'eog',
                        'EXG7':'ecg','EXG8':'emg'})
	
	#raw_f.plot(n_channels=72)
	
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

	events = mne.find_events(raw_fir, verbose=True)

	raw_fe=raw_fir.copy() # raw_fe was originally the 2 epoched data
	#raw_fe.plot()
	
	# # Looping through conditions, epoching # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # # #
	
	#event_msg=input('\n\n\n Please identify which alpha iteration you are working on [press enter to continue] ')
	
	if 1:
		con=1
		while con:
			iter_msg=input('which iteration do you want to use? (1-5, old versions) or 6: ')
			if iter_msg=='1': #sub15 was iter 1, but the timing was off anyway
				event_id={'target5_trig':105,'target8_trig':107,'dis5_trig':109,'dis8_trig':111} 
				con=0
			elif iter_msg=='2':
				event_id={}
				con=0
			elif iter_msg=='3':
				event_id={}
				con=0
			elif iter_msg=='4': # pretty sure the eeg I did was iter 4
				cue_event_id={'tarU3_trig':111,'tarB3_trig':113,'tarU9_trig':115,'tarB9_trig':117,
					'disU3_trig':119,'disU9_trig':121,'disB3_trig':123,'disB9_trig':125}  
				cue_tmin, cue_tmax = -0.5, 2  # 500 ms before event, and then 2 seconds afterwards. cue is .5 sec + 1.5 delay		
				probe_event_id={'probetrig':127}
				probe_tmin, probe_tmax=-0.5,2 # 2 second probe/response period
    				#tarinDist_trig=bytes([103])
    				#subNonRespTrig=bytes([105])
				#subRespTrig=bytes([107])
				#ITItrig=bytes([109])
				#'startSaveflag':254}
				con=0
			elif iter_msg=='5':#sub 44 was iter 5
				event_id={'distractor_trig':105,'neutral_trig':125,'target_trig':117} # making it up
					#[  105   107   109   117   125   127   131   133   254 65790]
				# this is totally wrong. iter 5 was flex&blocked, no Unilateral cues. have no idea what the codes are
					# i think the events are the same as iter 4, plus the addition of neutral conds
						# where neutralB_trig and neutralU_trig are 133 and 131 but idk which is which
				con=0
			elif iter_msg=='6':
				cue_event_id={'tarNdisLlocHLdisA_trig': 143, 'tarNdisHlocHRdisP_trig': 125, 'tarNdisHlocHLdisP_trig': 129, 'tarNdisHlocHLdisA_trig': 131, 'tarNdisLlocLdisP_trig': 145,  'tarNdisHlocHRdisA_trig': 127, 'tarNdisHlocLdisA_trig': 135,'tarNdisLlocHRdisP_trig': 137, 'tarNdisLlocHRdisA_trig': 139, 'tarNdisHlocLdisP_trig': 133, 'tarNdisLlocLdisA_trig': 147,  'tarNdisLlocHLdisP_trig': 141, } #'tarHdisLlocHLdisP_trig': 117, 'tarHdisLlocLdisA_trig': 123, 'tarHdisLlocHLdisA_trig': 119, 'tarHdisHlocHRdisA_trig': 103,'tarHdisHlocLdisA_trig': 111, 'tarHdisHlocHLdisP_trig': 105, 'tarHdisLlocHRdisA_trig': 115, 'tarHdisHlocHRdisP_trig': 101,'tarHdisLlocLdisP_trig': 121,'tarHdisLlocHRdisP_trig': 113, 'tarHdisHlocLdisP_trig': 109

				probe_event_id={'tarNdisIlocL_trig': 179, 'tarNdisVlocN_trig': 173, 'tarNdisIlocN_trig': 181, 'tarNdisVlocL_trig': 171, 'tarNdisIlocHV_trig': 175, 'tarNdisVlocHV_trig': 167 } #,'tarHdisIlocN_trig': 165, 'tarHdisVlocL_trig': 155, 'tarHdisVlocHV_trig': 151, 'tarHdisVlocHI_trig': 153,'tarHdisIlocL_trig': 163, 'tarHdisIlocHV_trig': 159, 'tarHdisVlocN_trig': 157, 'tarHdisIlocHI_trig': 161,'tarNdisIlocHI_trig': 177,'tarNdisVlocHI_trig': 169, }
				other_event_id={'stopSaveflag': 255, 'endofBlocktrig': 191, 'startSaveflag': 254, 'ITItrig': 189}
				response_event_id={'subResp_trig': 187, 'subNonResp_trig': 185}
				
				cue_tmin, cue_tmax = -0.8, 2.5  # 800 ms before event, and then 2.5 seconds afterwards. cue is 1 sec + 1.5 delay
				probe_tmin, probe_tmax = -0.8,2 # -800 and 2 second probe/response period 
				response_tmin,response_tmax=-0.5,1.5 # probably won't analyze this but might as well have it

				#FROM SPENSER: 
					#cue_event_id={'NLP_trig':119,'NLA_trig':121,'NHP_trig':123,'NHA_trig':125}
					#probe_event_id={'tarNdisVH_trig':131,'tarNdisVL_trig':103,'tarNdisIH_trig':137,'tarNdisIL_trig':139}
					#response_event_id={'subResp_Trig':107,'subNonResp_Trig':105}
					#other_event_id={'ITI_trig':109,'startSave_flag':254,'endofBlock_rig':133,'stopSave_flag':255}
				# 'HHP_trig':111,'HLP_trig':113,'HHA_trig':115,'HLA_trig':117,
				#'tarVdisIH_trig':133,'tarVdisIL_trig':135,'tarVdisVH_trig':127,'tarVdisVL_trig':129,, 
				# EXCLUDING THESE FOR NOW BC SPENSER DIDNT FINISH WHOLE EXP
				con=0
			else:
				print('oops, please enter an iteration')
	
	baseline = (None, -0.3) #baseline correction applied with mne.Epochs, this is starting @ beginning of epoch ie -0.8 
	epCond={}
	print('\n\n\n Epoching Conds \n ')
	#for event in cue_event_id.keys():
		#thisID={event:cue_event_id[event]}
	epCond['cue_events']=mne.Epochs(raw_fe, events=events, baseline=baseline, event_id=cue_event_id, tmin=cue_tmin,tmax=cue_tmax,metadata=behav_file)
	#for event in probe_event_id.keys():
		#thisID={event:probe_event_id[event]}
	epCond['probe_events']=mne.Epochs(raw_fe, events=events, baseline=baseline, event_id=probe_event_id, tmin=probe_tmin, tmax=probe_tmax,metadata=behav_file)
	#for event in response_event_id.keys():
		#thisID={event:response_event_id[event]}
	epCond['response_events']=mne.Epochs(raw_fe, events=events, baseline=(0,None), event_id=response_event_id, tmin=response_tmin, tmax=response_tmax,metadata=behav_file)
		# changed the baseline correction for this one because it doesn't make a whole lot of sense to baseline correct to -500 w a motor response?


	# # Inspect and reject bad epochs # # # # # # # # # # # #  # # # # # # # # # # 
	# # AND ICA on Raw data # # # # # # # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # # # # # 
	our_picks=mne.pick_types(raw_fe.info,meg=False,eeg=True,eog=False)#mne.pick_types(raw_fi.info,meg=False,eeg=True,eog=True,emg=True,stim=True,ecg=True)
 
	layout=mne.channels.read_montage('biosemi64')

	EOG_channels=['EXG3', 'EXG4', 'EXG5', 'EXG6']
	ECG_channels=['EXG7']

	for ev in epCond.keys():
		plotEpoch=1
		while plotEpoch:#while plotEpoch:
			print('plotting ' +ev)
			thisEp=[]
			thisEp=epCond[ev].copy()
			thisEp.load_data()
			print(thisEp)
			keep_plotting=1
			while keep_plotting:
				thisEp.plot(block=True, title=ev, n_epochs=5,n_channels=15)
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
	ask=1
	exit_loop=0
	while ask:	
		end_msg=input('Continue on to next sub? [y/n]')
		if end_msg=='y':
			continue
			ask=0
		elif end_msg=='n':
			exit_loop=1
			ask=0
		else:
			print('Oops! Please answer y/n')

	if exit_loop:
		break
#raw_f.info
#thispick=mne.pick_types(raw_fi.info,meg=False,eeg=True,eog=True,emg=True,stim=True,ecg=True)

# # Epoching into arbitrary 2-second windows # # # # # # # # # # # # # # # # # # # # # # # # # #
    # IVE COMMENTED THIS OUT BECAUSE OF THE ISSUES W/ RE-CONCAT INTO RAW FILE AFTER 2 SEC EPOCHING

#epoch_array=[]
#for t in raw_f.times[0::1024]:
 #   epoch_array.append([int(t),int(0),int(7)])  
    
#epoch_array=np.asarray(epoch_array)

#twoSec=mne.Epochs(raw_f,events=epoch_array,tmin=0,tmax=2,
	#event_id={'twoSec':7},picks=thispick)

#twoSec.plot(block=True) #selecting bad epochs to throw out
#twoSec.drop_bad()

#eps=[]
#for e in twoSec:
 #   eps.append(e)
#raw_fe=mne.io.RawArray(eps[0],raw_f.info)
#raw_ar=[]
#for ep in eps[1:]:
#    ep=mne.io.RawArray(ep,raw_f.info)
#    raw_ar.append(ep)
#raw_fe.append(raw_ar)

#eps[1]

##raw_f.info['events']
#event_ar=[]
#for event in events:
 #   sample=event[0]
#    if raw_fe.times[sample]==raw_f.times[sample]:
  #     one=sample
  #      event_ar.append([one,event[1],event[2]])
  #  else:
   #     try:
       #     one=list(raw_fe.times).index(raw_f.times[sample])
    #        event_ar.append([one,event[1],event[2]])
      #  except:
       #     continue
    
#raw_fe.info['events']=np.asarray(event_array)
#raw_fe.plot()



#raw_f.set_montage(layout)
#plottables={}
#epAfterICA={}
#for cond in epCond.keys():
 #   thisEp=epCond[cond]  
  #  thisEp_i=thisEp.copy()
   # thisEp_i.load_data()
    #thisEp_i.set_montage(layout)
    #icaCond=ICA(n_components=25,random_state=25)
    #icaCond.fit(thisEp_i,picks=our_picks)
    
    #eog_ic=[]
    #for ch in EOG_channels:  # find IC's attributable to EOG artifacts
     #   eog_idx,scores=icaCond.find_bads_eog(thisEp,ch_name=ch)
      #  eog_ic.append(eog_idx)
    #ecg_ic=[]
    #for ch in ECG_channels: # find IC's attributable to ECG artifacts
     #   ecg_idx,scores=icaCond.find_bads_ecg(thisEp,ch_name=ch)
      #  ecg_ic.append(ecg_idx)
    #reject_ic=[]
    #for eog_inds in eog_ic:
     #   for ele in eog_inds:
      #      if ele not in reject_ic:
       #         reject_ic.append(ele)
    #for ecg_inds in ecg_ic:
     #   for ele in ecg_inds:
      #      if ele not in reject_ic:
       #         reject_ic.append(ele) #add these IC indices to the list of IC's to reject
    
    #icaCond.exclude=[]
    #icaCond.exclude.extend(reject_ic)
    #icaCond.plot_components(picks=range(25),ch_type='eeg',inst=thisEp) 
    #bad_ics=[] #list those identified by visual inspection
    #icaCond.exclude.extend(bad_ics)
    #icaCond.apply(thisEp_i)
    #plottables[cond]=icaCond
    #epAfterICA[cond]=thisEp_i





#for cond in epCond.keys():
 #   thisEp=epCond[cond]
  #  thisEp.load_data()
   # # downsample???
    #thisEp.plot(block=True)
    #thisEp.drop_bad()
    #thisEp.info['bads']=[]
    # selecting bad electrodes
    #bads=[] #select bad electrodes by hand ? 
    #thisEp.info['bads']=bads
    #thisEp.interpolate_bads()
