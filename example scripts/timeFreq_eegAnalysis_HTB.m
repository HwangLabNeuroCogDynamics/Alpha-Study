clear all; clc; close all;

%% OPTIONS TO TWEAK
useLaplacian = 0;
baselineCorrect = 1;
plotSubtractions = 0;
runPlotter = 0;
mirrorFlag = 1;
lowerBoundFreq = 2;
upperBoundFreq = 50;
morletWaveletCycle = 6;

%% PATHS 
ROOT = '/home/despoC/HierarchyThetaBeta/EEG_Experiment/';
PROCEEG = [ROOT 'ProcEEG/'];
RESULTS = [ROOT 'ResultsEEG/'];
% version of this preprocessing pipeline
preprocVersion = 'oct2017';
% EEGLAB TOOLBOX
EEGLAB_TOOLBOX =  '/home/despoC/HierarchyThetaBeta/eeglab14_1_1b/';
addpath(EEGLAB_TOOLBOX);
% purge EEGLAB workspace
[ALLEEG,~,~] = eeglab('rebuild');
% RIDDLER TOOLBOX
RIDDLER_TOOLBOX = '/home/despoC/riddler/Riddler_Toolbox/';
addpath(genpath(RIDDLER_TOOLBOX));

% version
version = 'feb2018';

mkdir_JR(RESULTS);

%% SUBJECT INFO
SUBJECTS = {...
    '05','09','10','11',...
    '12','13','14','15',...
    '16','17','18','19',...
    '20','21','22','23'...
    '24','25','26','27',...
    '29','30','31','32',...
    '33','34','35','36',... '35',
    '37','38','39'};
SUBJECTS = {'35'};
numSub = length(SUBJECTS);

%% Task info
COND = {'R4','R8','D1','D2'};
numCond = length(COND);

%% EEG information
numChannels = 70;
numDataChannels = 64;
numExternals = 6;
% Question on what channels to run and display
channelsOfInterest = {'C3','C4','Cz','F3','F4','Fz','Pz','P3','P4','Oz','PO7','PO8'};
numChannelsOfInterest = length(channelsOfInterest);

bioSemiLocFile = '/home/despoC/HierarchyThetaBeta/Analysis_scripts/biosemi_64channel_6external.ced';
channelLocs = readlocs(bioSemiLocFile);
channelLabels = {channelLocs.labels};
channelsOfInterestIdxs = NaN(1,numChannelsOfInterest);
for chanIdx = 1:numChannelsOfInterest
    channelsOfInterestIdxs(chanIdx) = find(strcmpi(channelsOfInterest{chanIdx},channelLabels));
end

%% Spectral info
freqs = lowerBoundFreq:upperBoundFreq;
numFreqs = length(freqs);% steps in time for estimating spectral
spectralEstimateWindow = 20;
preStimulusTime = -1000;
postStimulusTime = 2000;
realTimesArray = preStimulusTime:spectralEstimateWindow:postStimulusTime;

%% Options
if useLaplacian
    laplacianPrefix = 'x';
else
    laplacianPrefix = 'p';
end
if baselineCorrect
    theBaseline = [3500 3700];
    baselineSuffix = '_baselineCorrect';
else
    theBaseline = NaN;
    baselineSuffix = '';
end
if plotSubtractions
    normalizeScale = 1;
else
    normalizeScale = NaN;
end
if runPlotter
    plotterStr = 'on';
else
    plotterStr = 'off';
end
if mirrorFlag
    mirrorStr = '_mirror';
else
    mirrorStr = '';
end

%% Load preprocessed data
for subIdx = 1:numSub
    subject = ['sub' SUBJECTS{subIdx}];
    SUBDIR = [PROCEEG subject '_' preprocVersion '/'];
    SUBRES = [RESULTS subject '/'];
    mkdir_JR(SUBRES);
    % output file
    timeFreqFile = [SUBRES 'timeFreq_' subject '_' num2str(numDataChannels) '_' laplacianPrefix 'files' baselineSuffix mirrorStr '_' version '.mat'];
    
    % purge EEGLAB workspace
    [ALLEEG,~,~] = eeglab('rebuild');
    
    % Check if time freq file already exists
    if exist(timeFreqFile,'file')~=2
        
        ersp_data = NaN(numCond,numDataChannels,numFreqs,3);
        % Loop through each condition and generate time frequency plots
        % make a single subplot of all 4 conditions
        for condIdx = 1:numCond
            cond = COND{condIdx};
            
            fprintf('\n\nRunning time frequency for %s %s\n\n\n',subject,cond);
            
            % Final preprocessed data
            if useLaplacian
                preprocFile = [SUBDIR 'xpalcb_' cond '_vfri' subject '_HTB.set'];
            else
                preprocFile = [SUBDIR 'palcb_' cond '_vfri' subject '_HTB.set'];
            end
            
            % load dataset
            EEG = pop_loadset('filename',preprocFile);
            [ALLEEG,EEG,CURRENTSET]=eeg_store(ALLEEG,EEG,0);
            
            % Mirror the data
            oldData = EEG.data;
            if mirrorFlag
                mirrorData = cat(2,flip(oldData,2),oldData,flip(oldData,2));
                mirrorTimesArray = 2000:20:5000; % it still knows about the epoching...
                EEG.pnts = EEG.pnts*3;
                EEG.data = mirrorData;
                [ALLEEG,EEG,CURRENTSET]=eeg_store(ALLEEG,EEG,0);
            else
                mirrorTimesArray = realTimesArray;
            end
            
            % loop through each channel of interest first
            for chanIdx = 1:numDataChannels
            
                if runPlotter
                    figure
                end
                % estimates time frequency plot
                % ERSP = event related spectral power
                [ersp,itc,powbase,times,freqs] = newtimef(...
                    EEG.data(chanIdx,:,:),... % run this for one channel at a time
                    EEG.pnts,...
                    [EEG.xmin EEG.xmax]*1000,... % min max signal
                    EEG.srate,... % sampling rate
                    morletWaveletCycle,... % from this frequencies use this number of wavelets [used to be lowest freq then wavelet]
                    'freqs',[lowerBoundFreq upperBoundFreq],...
                    'chaninfo',EEG.chaninfo,...
                    'nfreqs',numFreqs,... % number of frequencies to estimate
                    'elocs',channelLocs,... % channel locations
                    'timesout',mirrorTimesArray,... % when to run spectral with these as the center point
                    'baseline',theBaseline,...%[-500 0] or NaN,... % if you add a baseline then it changes the spectral estimate relative to that
                    'plotphase',plotterStr,...
                    'plotersp',plotterStr,...
                    'plotitc','off');
                
                numTimePoints = length(times);
                ersp_data(condIdx,chanIdx,:,1:numTimePoints)=ersp;
            end
        end
        save(timeFreqFile,'ersp_data');
    end
end

%% Analyzing intersting electrodes
% load all data
allERSP = NaN(numCond,numDataChannels,numFreqs,numTimePoints,numSub);
for subIdx = 1:numSub
    subject = ['sub' SUBJECTS{subIdx}];
    SUBRES = [RESULTS subject '/'];
    timeFreqFile = [SUBRES 'timeFreq_' subject '_' num2str(numDataChannels) '_' laplacianPrefix 'files' baselineSuffix '.mat'];
    thisSub_ersp = load(timeFreqFile);
    allERSP(:,:,:,:,subIdx) = thisSub_ersp.ersp_data;
end
            
for interestIdx = 1:numChannelsOfInterest
    
    chanIdx = channelsOfInterestIdxs(interestIdx);
    chanName = channelsOfInterest(interestIdx);
    
    figure
    if plotSubtractions

        R8_thisCondChan = squeeze(allERSP(2,chanIdx,:,:,:));
        R8_thisCondChan_avgERSP = mean(R8_thisCondChan,3);
        R4_thisCondChan = squeeze(allERSP(1,chanIdx,:,:,:));
        R4_thisCondChan_avgERSP = mean(R4_thisCondChan,3);
        D2_thisCondChan = squeeze(allERSP(4,chanIdx,:,:,:));
        D2_thisCondChan_avgERSP = mean(D2_thisCondChan,3);
        D1_thisCondChan = squeeze(allERSP(3,chanIdx,:,:,:));
        D1_thisCondChan_avgERSP = mean(D1_thisCondChan,3);
        subplot(2,2,1);
        tftopo(R8_thisCondChan_avgERSP' - R4_thisCondChan_avgERSP',times,freqs,...
            'logfreq','off', 'limits', [nan nan nan nan -normalizeScale normalizeScale]);
        colorbar;
        title(['R8 minus R4 ' chanName])

        subplot(2,2,2);
        tftopo(D2_thisCondChan_avgERSP' - D1_thisCondChan_avgERSP',times,freqs,...
            'logfreq','off', 'limits', [nan nan nan nan -normalizeScale normalizeScale]);
        colorbar;
        title(['D2 minus D1 ' chanName])



        subplot(2,2,3);
        tftopo(D2_thisCondChan_avgERSP' - R8_thisCondChan_avgERSP',times,freqs,...
            'logfreq','off', 'limits', [nan nan nan nan -normalizeScale normalizeScale]);
        colorbar;
        title(['D2 minus R8 ' chanName])


        subplot(2,2,4);
        tftopo(D1_thisCondChan_avgERSP' - R4_thisCondChan_avgERSP',times,freqs,...
            'logfreq','off', 'limits', [nan nan nan nan -normalizeScale normalizeScale]);
        colorbar;
        title(['D1 minus R4 ' chanName])
    else
        
        % plot each individually
        for condIdx = 1:numCond
            cond = COND{condIdx};
            
            thisCondChan = squeeze(allERSP(condIdx,chanIdx,:,:,:));
        	thisCondChan_avgERSP = mean(thisCondChan,3);
            subplot(2,2,condIdx);
            tftopo(thisCondChan_avgERSP',times,freqs,...
                'logfreq','off', 'limits', [nan nan nan nan -normalizeScale normalizeScale]);
            colorbar;
            title([cond ' ' chanName])
        end
    end
end
    