clear all; close all; clc;
%% PATHS 
ROOT = '/home/despoC/HierarchyThetaBeta/EEG_Experiment/';
PROCEEG = [ROOT 'ProcEEG/'];
RESULTS = [ROOT 'ResultsEEG/'];
% version of this preprocessing pipeline
preprocVersion = 'oct2017';
% EEGLAB TOOLBOX
EEGLAB_TOOLBOX =  '/home/despoC/HierarchyThetaBeta/eeglab14_1_1b/';
addpath(EEGLAB_TOOLBOX);
[ALLEEG,EEG,CURRENTSET] = eeglab('rebuild');
% RIDDLER TOOLBOX
RIDDLER_TOOLBOX = '/home/despoC/riddler/Riddler_Toolbox/';
addpath(genpath(RIDDLER_TOOLBOX));

mkdir_JR(RESULTS);

%% SUBJECT INFO
SUBJECTS = {...
    '05','09','10','11',...
    '12','13','14','15',...
    '16','17','18','19',...
    '20','21','22','23'...
    '24','25','26','27',...
    '29','30','31','32',...
    '33','34','35','36',...
    '37','38','39'};
% % SUBJECTS = {...
% %     '05','09','10','11',...
% %     '12','13','14','15', ...
% %     '16','17','18','19',...
% %     '20','21','22','23'};
    
numSub = length(SUBJECTS);

%% Task info
COND = {'R4','R8','D1','D2'};
numCond = length(COND);

for subIdx = 1:numSub
    subject = ['sub' SUBJECTS{subIdx}];
    
    SUB_PROC = [PROCEEG subject '_' preprocVersion '/'];
    
    allSets = cell(1,numCond);
    for condIdx = 1:numCond
        cond = COND{condIdx};
        postICA_file = [SUB_PROC 'palcb_' cond '_vfri' subject '_HTB.set'];
        allSets{condIdx} = postICA_file;
    end
    EEG = pop_loadset('filename',allSets);
    [ALLEEG,EEG,~]=pop_newset(ALLEEG,EEG,0,'study',0);
    EEG = eeg_checkset(EEG);
end
pop_comperp(ALLEEG,1,[4:4:(numSub*4), 3:4:(numSub*4)],[2:4:(numSub*4), 1:4:(numSub*4)],...
    'addavg','on',...
    'addstd','off',...
    'subavg','on',...
    'diffavg','off',...
    'diffstd','off',...
    'tplotopt',{'ydir',1});