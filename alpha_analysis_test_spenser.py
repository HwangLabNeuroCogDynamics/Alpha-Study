import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import average, std
from numpy.random import random, randint, normal, shuffle,uniform
import scipy
from scipy.stats import ttest_ind
import seaborn as sns
import fnmatch
import os  # handy system and path functions
import sys  # to get file system encoding
import csv
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd  
import matplotlib
print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)
import mne
#import FOOOF
from mne.time_frequency import tfr_morlet

ROOT='/data/backed_up/shared/AlphaStudy_data/EEG_preprocessed/'
behav_file='/home/dcellier/RDSS/AlphaStudy_Data/eegData/eeg_behavior_data/spenser_Feb_14_1502.csv'
behav=pd.read_csv(behav_file)
nhp_behav=behav[behav.disCue_validity==behav.disCue_validity[299]][behav.disCue=='Present'].reset_index(drop=True)

nla=mne.read_epochs(ROOT+'spenser/NLA-epo.fif') # no target, low distractor validity, absent cue
nha=mne.read_epochs(ROOT+'spenser/NHA-epo.fif')
nlp=mne.read_epochs(ROOT+'spenser/NLP-epo.fif')
nhp=mne.read_epochs(ROOT+'spenser/NHP-epo.fif') # no target, high dis cue validity, present

HHP=nhp[0:25]
HLP=nhp[25:50]

freqs = np.logspace(*np.log10([2, 35]), num=20)
n_cycles = freqs / 2.  # different number of cycle per frequency
power_HHP, itc = tfr_morlet(HHP, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1)
power_HLP, itc = tfr_morlet(HLP, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1)

#fig1, axis1 = plt.subplots(1, 2)
#fig2,axis2=plt.subplots(1,2)
#power_HHP.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
                 #  baseline=(-0.5, 0), mode='zscore', axes=axis1[0],
                   #title='Alpha-HHP(left)', show=False)
#power_HLP.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
                  # baseline=(-0.5, 0), mode='zscore', axes=axis1[1],
                   #title='Alpha-HLP', show=False)
#power_HHP.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=13, fmax=25,
                  # baseline=(-0.5, 0), mode='zscore', axes=axis2[0],
                  # title='Beta-HHP(left)', show=False)
#power_HLP.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=13, fmax=25,
                  # baseline=(-0.5, 0), mode='zscore', axes=axis2[1],
                  # title='Beta-HLP', show=False)
#power_HHP.plot_topo(baseline=(-0.5,0), mode='zscore', title='HHP')
#power_HLP.plot_topo(baseline=(-0.5,0), mode='zscore', title='HLP')

#raw_input('Move on?')
################

#power_nha, itc = tfr_morlet(nha, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                       # return_itc=True, decim=3, n_jobs=1)
#power_nhp, itc = tfr_morlet(nhp, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                       # return_itc=True, decim=3, n_jobs=1)
power_nhp_H, itc = tfr_morlet(nhp[0:25], freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1)
power_nhp_L, itc = tfr_morlet(nhp[25:50], freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1)
power_nhp_H.plot_topo(baseline=(-0.5,0), mode='zscore', title='NHP-high')
power_nhp_L.plot_topo(baseline=(-0.5,0), mode='zscore', title='NHP-low')

#fig1, axis1 = plt.subplots(1, 2)
#fig2,axis2=plt.subplots(1,2)
#power_nha.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
                 #  baseline=(-0.5, 0), mode='zscore', axes=axis1[0],
                 #  title='Alpha-NHA', show=False)
#power_nhp.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
                  # baseline=(-0.5, 0), mode='zscore', axes=axis1[1],
                  # title='Alpha-NHP', show=False)
#power_nha.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=13, fmax=25,
                #   baseline=(-0.5, 0), mode='zscore', axes=axis2[0],
                 #  title='Beta-NHA', show=False)
#power_nhp.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=13, fmax=25,
                #   baseline=(-0.5, 0), mode='zscore', axes=axis2[1],
                 #  title='Beta-NHP', show=False)
#power_nha.plot_topo(baseline=(-0.5,0), mode='zscore', title='NHA')
#power_nhp.plot_topo(baseline=(-0.5,0), mode='zscore', title='NHP')

#raw_input('Move on?')
###########

#power_nhp, itc = tfr_morlet(nhp, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                       # return_itc=True, decim=3, n_jobs=1)
power_nlp, itc = tfr_morlet(nlp, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1)
power_nlp_R, itc = tfr_morlet(nlp[0:25], freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1)
power_nlp_L, itc = tfr_morlet(nlp[25:50], freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1)

#fig1, axis1 = plt.subplots(1, 2)
#fig2,axis2=plt.subplots(1,2)
#fig3,axis3=plt.subplots(1,2)
#power_nlp.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
                 #  baseline=(-0.5, 0), mode='zscore', axes=axis1[0],
                 #  title='Alpha-NLP', show=False)
#power_nlp_R.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
              #     baseline=(-0.5, 0), mode='zscore', axes=axis3[1],
              #     title='Alpha-NLP(Right)', show=False)
#power_nlp_L.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
                #   baseline=(-0.5, 0), mode='zscore', axes=axis3[0],
                 #  title='Alpha-NLP(Left)', show=False)
#power_nhp.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
             #      baseline=(-0.5, 0), mode='zscore', axes=axis1[1],
              #     title='Alpha-NHP', show=False)
#power_nlp.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=13, fmax=25,
              #     baseline=(-0.5, 0), mode='zscore', axes=axis2[0],
              #     title='Beta-NLP', show=False)
#power_nhp.plot_topomap(ch_type='eeg', tmin=0.5, tmax=1.5, fmin=13, fmax=25,
       #            baseline=(-0.5, 0), mode='zscore', axes=axis2[1],
         #          title='Beta-NHP', show=False)
#power_nlp.plot_topo(baseline=(-0.5,0), mode='zscore', title='NLP')
#power_nhp.plot_topo(baseline=(-0.5,0), mode='zscore', title='NHP')

