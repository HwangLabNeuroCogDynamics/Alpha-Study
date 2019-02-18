#!/usr/bin/env python
# coding: utf-8

# In[2]:


import mne
from mne.datasets import sample
from mne import io
from mne.preprocessing import create_ecg_epochs, create_eog_epochs
from mne.preprocessing import ICA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[3]:


#from MNE tutorial
#data_path = sample.data_path()
#raw_fname= data_path + '/MEG/sample/sample_audvis_raw.fif'
#raw = mne.io.read_raw_fif(raw_fname, preload=True)


# In[4]:


#(raw.copy().pick_types(meg='mag')
#           .del_proj(0)
#           .plot(duration=60, n_channels=100, remove_dc=False))


# In[19]:


#now trying to import kai's test data
ROOT = '/home/dcellier/RDSS/AlphaStudy_Data/eegData/eeg_raw/'
raw_file=ROOT+'/realpeople/Dillan_Test1.bdf' #kai-test-2.bdf'
raw=mne.io.read_raw_edf(raw_file,montage='biosemi64',preload=True)


# In[20]:


#raw.plot_psd()


# # Filtering and re-referencing

# In[21]:


raw_f=raw.copy()
raw_f.filter(1,50)
raw_f.plot()


# In[22]:


raw_fr=raw_f.copy()
raw_fr, r2 = mne.set_eeg_reference(raw_fr,ref_channels=['EXG1','EXG2'])
externals=['EXG1','EXG2','EXG3','EXG4','EXG5','EXG6','EXG7','EXG8']

# In[23]:


print(raw_fr.info)
raw_fr.plot()


# # Defining Events
# 

# In[24]:


raw_fr.plot_psd(fmax=50,picks=mne.pick_types(raw_fr.info,eeg=True,exclude=externals))


# In[25]:


events = mne.find_events(raw, verbose=True)


# In[11]:


event_id = {'delay1trig':101,'probetrig':103,
            'target5trig':105,'target8trig':107,
            'dis5trig':109,'dis8trig':111,
            'neutraltrig':113,'ITItrig':115}
color= {101:'blue',103:'red',105:'grey',107:'green',
        109:'black',111:'yellow',113:'orange',115:'purple'}
mne.viz.plot_events(events,raw.info['sfreq'],raw.first_samp,color=color,event_id=event_id)


# In[12]:


event_id_t5 = {'target5trig':105}#,'target8trig':107} 
tmin, tmax = -0.5, 2  #dont remember the window, making this up
baseline = (None, 0.0)
epochs_tar5 = mne.Epochs(raw_fr, baseline=baseline, events=events, event_id=event_id_t5, tmin=tmin,
                    tmax=tmax)


# In[13]:


#epochs_tar5.plot(block=True)


# In[14]:


epochs_tar5.info


# # ICA

# In[15]:


our_picks=mne.pick_types(raw_fr.info,meg=False,eeg=True,eog=False,exclude=['EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG5', 'EXG6', 'EXG7', 'EXG8'])
#layout=mne.channels.read_layout(kind='biosemi64.lout', path='/home/dcellier/AlphaStudy_Analysis')
layout=mne.channels.read_montage('biosemi64')
raw_fr.set_montage(layout)
ica = ICA(n_components=25,random_state=25)
ica.fit(raw_fr,picks=our_picks)
layout.plot()


# In[20]:


#ica.plot_components(cmap='PiYG_r')
ica.info['bads']=[1]
ica.exclude


# In[17]:


ica.plot_components(picks=range(5),inst=raw_fr)


# # EOG artifact detection

# In[17]:


eog_epochs_3=create_eog_epochs(raw_fr,ch_name='EXG3',reject_by_annotation=False)
eog_inds3,scores=ica.find_bads_eog(eog_epochs_3,ch_name='EXG3')
eog_epochs_4=create_eog_epochs(raw_fr,ch_name='EXG4',reject_by_annotation=False)
eog_inds4,scores=ica.find_bads_eog(eog_epochs_4,ch_name='EXG4')
eog_epochs_5=create_eog_epochs(raw_fr,ch_name='EXG5',reject_by_annotation=False)
eog_inds5,scores=ica.find_bads_eog(eog_epochs_5,ch_name='EXG5')
eog_epochs_6=create_eog_epochs(raw_fr,ch_name='EXG6',reject_by_annotation=False)
eog_inds6,scores=ica.find_bads_eog(eog_epochs_6,ch_name='EXG6')


# In[18]:


eog_inds3


# In[19]:


scores


# In[20]:


eog_inds=[eog_inds3,eog_inds4,eog_inds5,eog_inds6]
ica.exclude=[]
for i in eog_inds:
    for ind in i:
        if ind not in ica.exclude:
            ica.exclude.extend([ind])
            #print ica.exclude


# In[1]:


ica.exclude


# In[22]:


#raw_fri.info


# In[23]:


#eog_average=eog_epochs_3.average()
#ica.plot_overlay(eog_average,exclude=)


# In[24]:


raw_fri=raw_fr.copy()
ica.apply(raw_fri)
raw_fri.plot()


# In[25]:


ica.plot_components(picks=range(10),inst=raw_fri)


# # ECG artifacts

# In[26]:


ecg_epochs_7=create_ecg_epochs(raw_fri,ch_name='EXG7')
ecg_inds,scores=ica.find_bads_ecg(ecg_epochs_7,ch_name='EXG7')


# In[27]:


ecg_inds


# In[28]:


ica.exclude.extend(ecg_inds)
ica.exclude


# In[29]:


ica.apply(raw_fri)


# In[30]:


ica.plot_overlay(raw_fr,ica.exclude)


# In[31]:


raw_fri.plot()


# In[32]:


ica.plot_components(picks=range(10),inst=raw_fri)


# # ICA to epoched data

# In[86]:


#epochs_tar5.load_data()
#epochs_tar5.plot(block=True)


# In[85]:


#epochs_tar5.set_montage(layout)
#ica_tar5 = ICA(n_components=25,random_state=25)
#ica_tar5.fit(epochs_tar5,picks=our_picks)


# In[84]:


#eog_inds=[eog_inds3,eog_inds4,eog_inds5,eog_inds6]
#ica_tar5.exclude=[]
#for i in eog_inds:
 #   for ind in i:
  #      if ind not in ica_tar5.exclude:
   #         ica_tar5.exclude.extend([ind])


# In[83]:


#ica_tar5.exclude


# In[82]:


#epochs_tar5_i=epochs_tar5.copy()
#ica_tar5.apply(epochs_tar5_i)
#epochs_tar5_i.plot()


# In[38]:


#TOMORROW: understand what the fit func is doing!
#ica_tar5.exclude.extend([0])
#ica_tar5.apply(epochs_tar5)


# In[81]:


#ica_tar5.plot_components(picks=range(10),inst=epochs_tar5_i)


# In[40]:


#ica_tar5.plot_sources(tar5_average,exclude=ica_tar5.exclude)


# In[41]:


#tar5_average.plot(exclude=['EXG1',"EXG2","EXG3",'EXG4',"EXG5","EXG6","EXG7",'EXG8'])


# In[80]:


#ica_tar5.plot_overlay(epochs_tar5.average(),exclude=ica_tar5.exclude)


# # Looping through conditions and applying ICA to them

# In[49]:


event_id = {'delay1trig':101,'probetrig':103,
            'target5trig':105,'target8trig':107,
            'dis5trig':109,'dis8trig':111,
            'neutraltrig':113,'ITItrig':115}

tmin, tmax = -0.5, 2  #dont remember the window, making this up
baseline = (None, 0.0)
epCond={}
for event in event_id.keys():
    thisID={event:event_id[event]}
    epCond[event]=mne.Epochs(raw_fr, events=events, event_id=thisID, tmin=tmin,
                    tmax=tmax)


# In[70]:


our_picks=mne.pick_types(raw_fr.info,meg=False,eeg=True,eog=False,exclude=['EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG5', 'EXG6', 'EXG7', 'EXG8'])
layout=mne.channels.read_montage('biosemi64')
raw_fr.set_montage(layout)
plottables={}
for cond in epCond.keys():
    thisEp=epCond[cond]
    thisEp_i=thisEp.copy()
    thisEp.load_data()
    thisEp_i.load_data()
    thisEp_i.set_montage(layout)
    icaCond=ICA(n_components=25,random_state=25)
    icaCond.fit(thisEp_i,picks=our_picks)
    icaCond.exclude=[0,3,5]
    icaCond.apply(thisEp_i)
    plottables[cond]=icaCond


# In[67]:


#event_id = {'delay1trig':101,'probetrig':103,
#            'target5trig':105,'target8trig':107,
 #           'dis5trig':109,'dis8trig':111,
  #          'neutraltrig':113,'ITItrig':115}
def plot_diff(epoch,ica):
    return ica.plot_overlay(epoch.average(),exclude=ica.exclude)


# In[72]:


plot_diff(epCond['delay1trig'],plottables['delay1trig'])


# In[73]:


plot_diff(epCond['probetrig'],plottables['probetrig'])


# In[74]:


plot_diff(epCond['target5trig'],plottables['target5trig'])


# In[75]:


plot_diff(epCond['target8trig'],plottables['target8trig'])


# In[76]:


plot_diff(epCond['dis5trig'],plottables['dis5trig'])


# In[77]:


plot_diff(epCond['dis8trig'],plottables['dis8trig'])


# In[78]:


plot_diff(epCond['neutraltrig'],plottables['neutraltrig'])


# In[79]:


plot_diff(epCond['ITItrig'],plottables['ITItrig'])


# In[ ]:




