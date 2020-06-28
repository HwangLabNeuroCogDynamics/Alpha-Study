clear all; close all; clc;
%% PATHS 
ROOT = '/home/despoC/HierarchyThetaBeta/EEG_Experiment/';
RAWEEG = [ROOT 'RawEEG/'];
PROCEEG = [ROOT 'ProcEEG/'];
BEHAV = [ROOT 'Behavior/'];
% version of this preprocessing pipeline
version = 'oct2017';
% EEGLAB TOOLBOX
EEGLAB_TOOLBOX =  '/home/despoC/HierarchyThetaBeta/eeglab14_1_1b/';
addpath(EEGLAB_TOOLBOX);
[ALLEEG,EEG,CURRENTSET] = eeglab('rebuild');
% RIDDLER TOOLBOX
RIDDLER_TOOLBOX = '/home/despoC/riddler/Riddler_Toolbox/';
addpath(genpath(RIDDLER_TOOLBOX));

%% SUBJECT INFO
% check on sub21 - some problem with epoching
%i think this is the subject hat stopped
%after the first few trials and started again 
% markers are messed up
SUBJECTS = {...
    '05','09','10','11',... 
    '12','13','14','15',...
    '16','17','18','19',...
    '20','21','22','23'...
    '24','25','26','27',...
    '29','30','31','32',...
    '33','34','35','36',...
    '37','38','39'};
%SUBJECTS = {'35'};

numSub = length(SUBJECTS);

%% Task info
numBlocks = 8;
numTrials = 48;
COND = {'R4','R8','D1','D2'};
numCond = length(COND);
convertToNumber = {'R4',111,'R8',112,'D1',113,'D2',114,...
    'ErrR4',115,'ErrR8',116,'ErrD1',117,'ErrD2',118,...
    'Miss',119,...
    'R4rt',121,'R8rt',122,'D1rt',123,'D2rt',124,...
    'ErrR4rt',125,'ErrR8rt',126,'ErrD1rt',127,'ErrD2rt',128,...
    'Missrt',129,...
    };
conVal = {111, 112, 113, 114};

%% EEG info 
bioSemiLocFile = '/home/despoC/HierarchyThetaBeta/Analysis_scripts/biosemi_64channel_6external.ced';
samplingRate = 1024;
numChannels = 64;
numExternals = 6;
leftMastoid_ELECTRODE = 65;
rightMastoid_ELECTRODE = 66;
referenceElectrodes = [leftMastoid_ELECTRODE rightMastoid_ELECTRODE];
numReferenceExternals = length(referenceElectrodes);
baseline_TIME = 1;
postStim_TIME = 2;
numElectrodes = numChannels + numExternals;
numElectrodesMinRef = numElectrodes - numReferenceExternals;
% when does the baseline start relative to the epoch start
baselineStart = - baseline_TIME * 1000;
baselineEnd = 0;
% tiny baseline
tinyBaseline = -200;
highPassFilter = 0.5;
lowPassFilter = 100;

%% Start loop through subjects
for subIdx = 1:numSub
    
    % info for this subject
    subject = ['sub' SUBJECTS{subIdx}];
    SUB_BEHAV = [BEHAV subject '/'];
    SUBPROC = [PROCEEG subject '_' version '/'];
    mkdir_JR(SUBPROC);
    
    % Raw EEG file for this subject
    fileNameRoot = [subject '_HTB'];
    eegFile = [RAWEEG fileNameRoot '.bdf'];
    
    % Behav file
    behavFndr = dir([SUB_BEHAV 'results_HTB_' subject '_EEG_*.mat']);
    numBlocksFound = length(behavFndr);
    
    % check if files exist
    runPreproc = 0;
    if exist(eegFile,'file')==2 && numBlocksFound >= 8
        runPreproc = 1;
    end
    firstFile = [SUBPROC 'i' fileNameRoot '.set'];
    if exist(firstFile,'file')==2
        runPreproc = 1;
    end
    
    % if the files exists to conduct analysis then dive in
    if ~runPreproc
        fprintf('Missing EEG data or results files for %s\n\n\n\n',subject);
    else
        fprintf('Running EEG preprocessing on %s\n\n\n\n',subject);
        %% Step 1: import the data
        prefix = 'i';
        procFilename = [prefix fileNameRoot '.set'];
        importEEG_file = [SUBPROC procFilename];
        if exist(importEEG_file,'file')==2
            fprintf('Skipping data import for %s\n\n',subject);
        else
            fprintf('Running data input for %s\n\n',subject);
            EEG = pop_biosig(eegFile);
            EEG.chanlocs = readlocs(bioSemiLocFile);
            EEG.chanlocs = EEG.chanlocs(1:numElectrodes);
            EEG.nbchan = numElectrodes;
            EEG.chaninfo.nosedir = '-X';
            EEG.data = EEG.data(1:numElectrodes,:);
            [ALLEEG,EEG,CURRENTSET]=pop_newset(ALLEEG,EEG,length(ALLEEG),'savenew',importEEG_file,'gui','off');
        end
        
        
        %% Step 2: Re-refrencing the data
        % tell the system what the reference is
        prefix = 'r';
        procFilename = [prefix procFilename];
        rerefEEG_file = [SUBPROC procFilename];
        if exist(rerefEEG_file,'file')==2
            fprintf('Skipping re-referencing for %s\n\n',subject);
        else
            fprintf('Running re-referencing for %s\n\n',subject);
            EEG = pop_loadset(importEEG_file);
            EEG = pop_reref(EEG, referenceElectrodes);
            %save(rerefEEG_file,'EEG');
            [ALLEEG,EEG,CURRENTSET]=pop_newset(ALLEEG,EEG,length(ALLEEG),'savenew',rerefEEG_file,'gui','off');
        end
        
        %% Step 3: Filter the Data - high pass
        prefix = 'f';
        procFilename = [prefix procFilename];
        filterEEG_file = [SUBPROC procFilename];
        if exist(filterEEG_file,'file')==2
            fprintf('Skipping data filter for %s\n\n',subject);
        else
            fprintf('Running data filter for %s\n\n',subject);
            EEG = pop_loadset(rerefEEG_file);
            EEG = pop_eegfilt(EEG,highPassFilter,0,[],0);
            EEG = pop_eegfilt(EEG,0,lowPassFilter,[],0);
            %save(filterEEG_file,'EEG');
            [ALLEEG,EEG,CURRENTSET]=pop_newset(ALLEEG,EEG,length(ALLEEG),'savenew',filterEEG_file,'gui','off');
        end
        
        %% Step 4: Label events in the data
        prefix = 'v';
        procFilename = [prefix procFilename];
        eventEEG_file = [SUBPROC procFilename];
        if exist(eventEEG_file,'file')==2
            fprintf('Skipping event labels for %s\n\n',subject);
        else
            fprintf('Running event labels for %s\n\n',subject);
            EEG = pop_loadset(filterEEG_file);
            if strcmp(subject,'sub35') % event types are strings for this subject - convert back to doubles
                numEvents = length(EEG.event);
                eventMarkers = NaN(1,numEvents);
                for eventIdx = 1:numEvents
                    eventMarkers(eventIdx) = str2double(EEG.event(eventIdx).type);
                end
            else
                eventMarkers = [EEG.event.type];
            end
            numEvents = length(eventMarkers);
            stimulusAppears = 5;
            stimIdxs = find(eventMarkers == stimulusAppears);
            
            % rename to R4,R8,D1,D2,R4err,R8err,D1err,D2err,Miss
            allTrialsCounter = 0;
            for blockIdx = 1:numBlocks
                behavFndr = dir([SUB_BEHAV 'results_HTB_' subject '_EEG_' num2str(blockIdx) '_*.mat']); 
                behavFile = [SUB_BEHAV behavFndr(1).name];
                behavResults = load(behavFile);
                trialInfo = behavResults.trialInfo;
                for trialIdx = 1:numTrials
                    thisTrial = trialInfo(trialIdx);
                    allTrialsCounter = allTrialsCounter + 1;
                    if thisTrial.correct
                        errPrefix = '';
                    else
                        errPrefix = 'Err';
                    end
                    thisRT = thisTrial.reactionTime;
                    eventIdx = stimIdxs(allTrialsCounter);
                    thisEvent = EEG.event(eventIdx);
                    if isnan(thisRT)
                        trialName = 'Miss';
                        thisRT = 2; % if no RT just set it as the full response window
                    else
                        trialName = [errPrefix thisTrial.condition];
                    end
                    trialVal = convertToNumber{find(strcmp(convertToNumber,trialName))+1};
                    EEG.event(eventIdx).type = trialVal;
                    rtLatency = thisEvent.latency + round(samplingRate * thisRT);
                    newEventIdx = numEvents + allTrialsCounter;
                    newTrialName = [trialName 'rt'];
                    newTrialVal = convertToNumber{find(strcmp(convertToNumber,newTrialName))+1};
                    if strcmp('sub35',subject)
                        EEG.event(newEventIdx) = struct(...
                            'type',newTrialVal,...
                            'latency',rtLatency,...
                            'urevent',newEventIdx,...
                            'duration',0);
                    else
                        EEG.event(newEventIdx) = struct(...
                            'type',newTrialVal,...
                            'latency',rtLatency,...
                            'urevent',newEventIdx);
                    end
                end
            end
            %save(eventEEG_file,'EEG');
            [ALLEEG,EEG,CURRENTSET]=pop_newset(ALLEEG,EEG,length(ALLEEG),'savenew',eventEEG_file,'gui','off');
        end
        
        %% Step 5: Epoch and save each condition as a separate dataset
        condSetFiles = cell(1,numCond);
        for condIdx = 1:numCond
            condName = COND{condIdx};
            condValue = conVal(condIdx);
            
            condSetFile = [SUBPROC condName '_' procFilename(1:end-4) '.set'];
            condSetFiles{condIdx} = condSetFile;
            if exist(condSetFile,'file')==2
                fprintf('Skipping epoching for %s %s\n\n',subject,condName);
            else
                fprintf('Running epoching for %s %\n\n',subject,condName);
                EEG = pop_loadset(eventEEG_file);
                EEG = pop_epoch(EEG,condValue,[-baseline_TIME postStim_TIME]);
                [ALLEEG,EEG,CURRENTSET]=pop_newset(ALLEEG,EEG,length(ALLEEG),'savenew',condSetFile,'gui','off');
            end
        end
        
        %% Step 6: Remove baseline - mean adjustment of the overall signal - set signal to 0 for ERP sake
        condSet_noBase_files = cell(1,numCond);

        epochPrefix = 'b_';
        for condIdx = 1:numCond
            condName = COND{condIdx};
            condSet_noBase = [SUBPROC epochPrefix condName '_' procFilename(1:end-4) '.set'];
            condSet_noBase_files{condIdx} = condSet_noBase;
            if exist(condSet_noBase,'file') ==2
                fprintf('Skipping baseline removal for %s %s\n\n',subject,condName);
            else
                [ALLEEG,EEG,CURRENTSET] = eeglab('rebuild');
                fprintf('Running baseline removal for %s %\n\n',subject,condName);
                EEG = pop_loadset('filename',condSetFiles{condIdx});
                EEG = pop_rmbase( EEG, [baselineStart baselineEnd]);
                [ALLEEG,EEG,CURRENTSET]=pop_newset(ALLEEG,EEG,length(ALLEEG),'savenew',condSet_noBase,'gui','off');                
            end
        end
        
        %% Step 7: Reject "crap" data
        condSet_reject_files = cell(1,numCond);
        prefix = 'c';
        epochPrefix = [prefix epochPrefix];
        for condIdx = 1:numCond
            condName = COND{condIdx};
            condSet_reject = [SUBPROC epochPrefix condName '_' procFilename(1:end-4) '.set'];
            condSet_reject_files{condIdx} = condSet_reject;
            if exist(condSet_reject,'file')==2
                fprintf('Skipping trial rejection for %s %s\n\n',subject,condName);
            else
                fprintf('Running trial rejection for %s %\n\n',subject,condName);
                EEG = pop_loadset('filename',condSet_noBase_files{condIdx});
                [ALLEEG,EEG,~] = eeg_store(ALLEEG,EEG);
                
                rejectTrialsFile = [SUBPROC condName '_rejectTrials.mat'];
                if exist(rejectTrialsFile,'file')~=2
                    EEG = eeg_checkset(EEG);
                    pop_eegplot(EEG,1,1,1);
                    validAnswer = 0;
                    while ~validAnswer
                        trialsToReject = input(sprintf('Which trials are you rejecting for %s? (e.g. 12,25,34,... or none): ',condName),'s');
                        if strcmpi(trialsToReject,'none')
                            trialsToReject = [];
                            validAnswer = 1;
                        else
                            trialsToReject = regexp(trialsToReject,',','split');
                            trialsToReject = str2double(trialsToReject);
                            if ~isnan(trialsToReject)
                                validAnswer = 1;
                            end
                        end
                    end
                    save(rejectTrialsFile,'trialsToReject');
                else
                    load(rejectTrialsFile);
                end
                % command that actually removes reject trials
                if ~isempty(trialsToReject)
                    EEG = pop_rejepoch(EEG,trialsToReject,0);
                end
                [ALLEEG,EEG,~]=pop_newset(ALLEEG,EEG,length(ALLEEG),'savenew',condSet_reject,'gui','off');
                eeglab redraw;
            end
        end
        
        
        
        %% Step 8: Visually inspect and interpolate electrodes
        condSet_interp_files = cell(1,numCond);
        prefix = 'l';
        epochPrefix = [prefix epochPrefix];
        interpolationFile = [SUBPROC 'interpolatedElectrodes.mat'];
        if exist(interpolationFile,'file')==2
            fprintf('Skipping eletrode inspection for %s\n\n',subject);
            load(interpolationFile);
        else
            fprintf('Running electrode inspection for %s\n\n',subject);
            
            validAnswer = 0;
            while ~validAnswer
                elecToInterpStr = input(sprintf('Which electrodes need to be interpolated (e.g. "none" or "1,6,10"): '),'s');
                if strcmp(elecToInterpStr,'none')
                    validAnswer = 1;
                    elecToInterp = NaN;
                else
                    elecToInterp = regexp(elecToInterpStr,',','split');
                    elecToInterp = str2double(elecToInterp);
                    if isempty(find(isnan(elecToInterp),1))
                        validAnswer = 1;
                    else
                        fprintf('invalid response, try again...\n\n\n\n');
                    end
                end
            end
            save(interpolationFile,'elecToInterp');
        end
            
        for condIdx = 1:numCond
            condName = COND{condIdx};
            condSet_interp = [SUBPROC epochPrefix condName '_' procFilename(1:end-4) '.set'];
            condSet_interp_files{condIdx} = condSet_interp;
            if exist(condSet_interp,'file')==2
                fprintf('Skipping electrode interpolation for %s %s\n\n',subject,condName);
            else
                fprintf('Running electrode interpolation for %s %s\n\n',subject,condName);
                EEG = pop_loadset('filename',condSet_reject_files{condIdx});
                EEG.chanlocs = readlocs(bioSemiLocFile);
                EEG.chanlocs = EEG.chanlocs(1:numElectrodesMinRef);
                [ALLEEG,EEG,~] = eeg_store(ALLEEG,EEG);

                if ~isnan(elecToInterp)
                    EEG = eeg_interp(EEG,elecToInterp);
                end
                [ALLEEG,EEG,CURRENTSET]=pop_newset(ALLEEG,EEG,length(ALLEEG),'savenew',condSet_interp,'gui','off');
            end
        end
        
        
        %% Step 9: Independent Component Analysis
        condSet_ica_files = cell(1,numCond);
        prefix = 'a';
        epochPrefix = [prefix epochPrefix];
        for condIdx = 1:numCond
            condName = COND{condIdx};
            condSet_ica = [SUBPROC epochPrefix condName '_' procFilename(1:end-4) '.set'];
            condSet_ica_files{condIdx} = condSet_ica;
            if exist(condSet_ica,'file')==2
                fprintf('Skipping ICA for %s %s\n\n',subject,condName);
            else
                [ALLEEG,EEG,CURRENTSET] = eeglab('rebuild');
                fprintf('Running ICA for %s %\n\n',subject,condName);
                EEG = pop_loadset('filename',condSet_interp_files{condIdx});
                [ALLEEG,EEG,~] = eeg_store(ALLEEG,EEG);
                
                % run ica
                EEG = pop_runica(EEG,'icatype','runica','extended',1);
                % save it out
                [ALLEEG,EEG,~]=pop_newset(ALLEEG,EEG,length(ALLEEG),'savenew',condSet_ica,'gui','off');
                eeglab redraw;
            end
        end
        
        %% Step 10: Manually inspect the ICA and reject components
        condSet_postICA_files = cell(1,numCond);
        prefix = 'p';
        epochPrefix = [prefix epochPrefix];
        for condIdx = 1:numCond
            condName = COND{condIdx};
            condSet_postICA = [SUBPROC epochPrefix condName '_' procFilename(1:end-4) '.set'];
            condSet_postICA_files{condIdx} = condSet_postICA;
            if exist(condSet_postICA,'file')==2
                fprintf('Skipping IC removal for %s %s\n\n',subject,condName);
            else
                fprintf('Running IC removal for %s %\n\n',subject,condName);
                EEG = pop_loadset('filename',condSet_ica_files{condIdx});
                [ALLEEG,EEG,~] = eeg_store(ALLEEG,EEG);
                
                icsRemovedFile = [SUBPROC condName '_ICsRemoved.mat'];
                if exist(icsRemovedFile,'file')~=2
                    pop_selectcomps(EEG,1:35);
                    validAnswer = 0;
                    while ~validAnswer
                        icsToRmStr = input(sprintf('%s Which ICs need to be removed for %s? (e.g. "none" or "1,6,10"): ',subject,condName),'s');
                        if strcmp(icsToRmStr,'none')
                            validAnswer = 1;
                            elecToInterp = NaN;
                        else
                            icsToRmStr = regexp(icsToRmStr,',','split');
                            icsToRm = str2double(icsToRmStr);
                            if isempty(find(isnan(icsToRm),1))
                                validAnswer = 1;
                            else
                                fprintf('invalid response, try again...\n\n\n\n');
                            end
                        end
                    end
                    save(icsRemovedFile,'icsToRm');
                else
                    load(icsRemovedFile);
                end
                if ~isnan(icsToRm)
                    EEG = pop_subcomp(EEG,icsToRm);
                end
                % remove the baseline after running ica
                EEG = pop_rmbase(EEG, [tinyBaseline 0]);
                EEG.chanlocs = EEG.chanlocs(1:numChannels);
                EEG.nbchan = numChannels;
                EEG.chaninfo.nosedir = '-X';
                EEG.data = EEG.data(1:numChannels,:,:);
                % save it out
                [ALLEEG,EEG,CURRENTSET]=pop_newset(ALLEEG,EEG,length(ALLEEG),'savenew',condSet_postICA,'gui','off');
            end
        end
    end
end
