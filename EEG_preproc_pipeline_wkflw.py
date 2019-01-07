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
#import ipywidgets
#from ipywidgets import widgets


#import kai's test data
ROOT = '/home/dcellier/RDSS/AlphaStudy_Data/eegData/'
ROOT_raw=ROOT+'eeg_raw/'
ROOT_proc=ROOT+'eeg_preproc/'
subject_files=[]
for filename in os.listdir(ROOT_raw): #compiling the subjects downloaded from MIPDB
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
	raw=mne.io.read_raw_edf(raw_file,montage=mne.channels.read_montage('biosemi64'),preload=True)
	#raw.plot(n_channels=72)

	# # Re-reference, apply high and low pass filters (1 and 50) # # # # # # # # # #

	raw_f=raw.copy()
	raw_f,r= mne.set_eeg_reference(raw_f,ref_channels=['EXG1', 'EXG2'])#,'EXG8'])#mastoids, nose -- nose we decided we didn't want to use to reref
	raw_f.set_channel_types({'EXG1':'emg','EXG2':'emg','EXG3':'eog','EXG4':'eog','EXG5':'eog','EXG6':'eog',
                        'EXG7':'ecg','EXG8':'emg'})
	raw_f.filter(1,50)
	#raw_f.plot(n_channels=72)
	
		# # # # # # selecting bad electrodes # # # # # #	
	raw_fi=raw_f.copy()
        raw_DataCH=(raw_fi.copy()).drop_channels(['EXG1', 'EXG2','EXG3','EXG4','EXG5','EXG6','EXG7','EXG8'])
        tryAgain=1
        while tryAgain:
		raw_DataCH.plot(block=True) #pauses script while i visually inspect data and select which channels to delete
                bads=raw_DataCH.info['bads']
                text_msg2=raw_input('The channels you marked as bad are: '+str(bads)+' \n Are you ready to interpolate? [y/n]: ')
                if text_msg2=='y':
                        raw_fi.info['bads']=bads
                        raw_fi=raw_fi.interpolate_bads()
                        tryAgain=0
                elif text_msg2=='n':
                        tryAgain=1	
                else:
                        print('invalid entry: '+text_msg2)
                        tryAgain=1

	# # Finding Events (triggers) # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	events = mne.find_events(raw_fi, verbose=True)

	raw_fe=raw_fi.copy() # raw_fe was originally the 2 epoched data
	#raw_fe.plot()

	# # ICA on Raw data # # # # # # # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # # # # # 

	EOG_channels=['EXG3', 'EXG4', 'EXG5', 'EXG6']
	ECG_channels=['EXG7']

	our_picks=mne.pick_types(raw_fe.info,meg=False,eeg=True,eog=False)#mne.pick_types(raw_fi.info,meg=False,eeg=True,eog=True,emg=True,stim=True,ecg=True)
 
	layout=mne.channels.read_montage('biosemi64')
	raw_fe.set_montage(layout)
	ica=ICA(n_components=25,random_state=25,method='infomax')
	ica.fit(raw_fe,picks=our_picks)

	eog_ic=[]
	for ch in EOG_channels:
		# find IC's attributable to EOG artifacts
		eog_idx,scores=ica.find_bads_eog(raw_fe,ch_name=ch)
		eog_ic.append(eog_idx)
	ecg_ic=[]
	for ch in ECG_channels: # find IC's attributable to ECG artifacts
		ecg_idx,scores=ica.find_bads_ecg(raw_fe,ch_name=ch)
		ecg_ic.append(ecg_idx)
	reject_ic=[]
	for eog_inds in eog_ic:
		for ele in eog_inds:
			if ele not in reject_ic:
				reject_ic.append(ele)
	for ecg_inds in ecg_ic:
		for ele in ecg_inds:
			if ele not in reject_ic:
				reject_ic.append(ele) #add these IC indices to the list of IC's to reject
    
	ica.exclude=[]
	ica.exclude.extend(reject_ic)

	plot=1
	while plot:  
		ica.plot_components(picks=range(25),ch_type=None,cmap='interactive',inst=raw_fe)# changed to ch_type=None from ch_type='EEG'because this yielded an error
		#while len(ica.exclude)==len(reject_ic):
		#	continue
		ica.plot_overlay(raw_fe,exclude=ica.exclude)
		verification_ic=raw_input('The ICs marked for rejection are: ' + str(ica.exclude) +'\n Are you sure you want to proceed? [y/n]: ')
		if verification_ic=='y':
			#ica.exclude.extend(bad_ics)
			plot=0
		else:
			print('Please select which ICs you would like to reject')
		#ica.plot_components(picks=range(25),ch_type=None,inst=thisEp)  
	raw_fei=raw_fe.copy()
	ica.apply(raw_fei)
	raw_fei.drop_channels(['EXG1', 'EXG2','EXG3','EXG4','EXG5','EXG6','EXG7','EXG8'])

	# # Looping through conditions, epoching # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # # #
	
	event_msg=raw_input('\n\n\n ATTENTION !!!!!!!!!!!!!!!!! \n events assuming alpha pilot 1 iter 1 \n\n\n Continue?  [y/n]: ')
	if event_msg=='y':
		event_id = {'target5_trig':105,'target8_trig':107,'dis5_trig':109,'dis8_trig':111}
		#{#'delay1trig':101,'probetrig':103, .....
  	          #'neutraltrig':113,'ITItrig':115}
	elif event_msg=='n':
		con=1
		while con:
			iter_msg=raw_input('which iteration do you want to use? (1-5) or 6: ')
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
				event_id={'tarU3_trig':111,'tarB3_trig':113,'tarU9_trig':115,'tarB9_trig':117,
					'disU3_trig':119,'disU9_trig':121,'disB3_trig':123,'disB9_trig':125}    				
				#probetrig=bytes([127])
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
			else:
				print('oops, please enter an iteration')

	tmin, tmax = -0.5, 2  #dont remember the window, making this up
	baseline = (None, 0.0) #baseline correction applied with mne.Epochs, this is starting @ beginning of epoch ie -0.5 
	epCond={}
	for event in event_id.keys():
		thisID={event:event_id[event]}
		epCond[event]=mne.Epochs(raw_fei, events=events, baseline=baseline, event_id=thisID, tmin=tmin,tmax=tmax)

	# # Inspect and reject bad epochs # # # # # # # # # # # #  # # # # # # # # # # 

	for ev in epCond.keys():
		plotEpoch=1
	        while plotEpoch:
			thisEp=[]
			thisEp=epCond[ev].copy()
	               	thisEp.plot(block=True)
	               	bads=raw_input('Are you sure you want to continue? [y/n]')
			if bads=='y':
				#ep=ep.drop_bad()
				epCond[ev]=thisEp
				plotEpoch=0
			elif bads=='n':
				continue
			else:
				print('oops, please indicate which epochs you would like to reject')
	

	print('\n\n\n\n SAVING OUT INFO ~~~~~~~ \n\n')
	save_path=ROOT_proc+sub_name+'/'
	os.mkdir(save_path)
	def save_object(obj,filename):
		with open(filename,'wb') as output:
			pickle.dump(obj,output,pickle.HIGHEST_PROTOCOL)

	for event in event_id.keys():
		event_name=event.split('_')[0]
		thisEp=epCond[event]
		save_object(thisEp,filename=save_path+event_name)
	ask=1
	exit_loop=0
	while ask:	
		end_msg=raw_input('Continue on to next sub? [y/n]')
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
