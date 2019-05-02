function compoThresh(subjInitials, p)
% function compoThresh(subjInitials,p)
% This function is to generate component motion stimulus and measure the
% duration threshold for a subject to perform a 2AFC directional judgment task

% Input:
%   <subjInitials>: subject initials, like "RZ". For data naming
%   <p>: a structure for structures, it contains the fields:
%       <speed>: deg/sec;
%       <contrast>: %, 0~100;

if notDefined('subjInitials')
    error('You must input subject initials')
end
if notDefined('p')
    p.contrast = 50;
    p.speed = 4;
end

try
    warning('off','MATLAB:dispatcher:InexactMatch');
    KbName('UnifyKeyNames');
    
    %% --------------- key parameters--------------
    contrast = p.contrast; % contrast 
    speed = p.speed; % deg/sec
    
    %% --------------- Monitor Parameters -----------------
    
    %%%%%%%%%%%%%%%%%%%%%%% Experimenter scale_factor here %%%%%%%%
    % most important parameter - how many acrmin is one screen pixel?
    scale_factor = 2.00;
    %%%%%%%%%%%%%%%%%%%%%%% Experimenter scale_factor here %%%%%%%%
    frameRate = 120;       %
    %% -------- other STIMULI parameters-------------------------------
    radius = 8;  % deg
    orientation = 0; % we always present left right motion
    SF                     = 1;        %cycles/deg
    which_envelope 	       = 2;
    background             = 127;      %background intensity, in gray scale untis
    cpfov = radius * 2 * SF;
    TFstep = 2*pi*SF*speed/frameRate; % temporal frequency step
    amplitude = 127 * contrast/100;
    %% ------- other exp parameters ----------------
    nTrials = 160; % Number of trials for each staircase
    cuexy1=[3 40 35 40 35 40;
        0 0 -5 0 5 0];
    cuexy1=[cuexy1 -cuexy1];% for, orientation==0
    
    %% ---------- initialize staircase -------------
    upper_limit              = 400;       % ms
    start_point              = [110 100]; % ms
    stair_consecutive        = 1;         % 1 means conventional staircase design. n consecutive up is up. 0 mean every n up is up. we can set different percentage correct by choosing different design.
    up_down_step_in_log      = 0.1;       % step size log unit
    
    if stair_consecutive == 1
        up_down_design = [ 1,2; 1,3; ];%% [up, down].  % because 2AFC, we use 2/1 and 3/1 staircases
    else
        up_down_design = [ 2,1; 1,2; 1,7 ];%%% [up, down].
    end
    curr_up_downs  = zeros( size( up_down_design) );
    curr_stair_t   = start_point;
    
    %% create data structure    
    total_trials = nTrials*size(up_down_design,1);  %per block
    data = zeros(total_trials,8);% trial number,staircase number, contrast, size, direction, duration, choice, correct
    a = getranddesign(total_trials,[2,2]); % 2 staricases * 2 direction
    data(:,1) = a(:,1); % trial number
    data(:,2) = a(:,2); % staircase index
    data(:,3) = contrast;
    data(:,4) = radius;
    data(:,5) = a(:,3); % direction
    
    %% open Screen windows and show instruction and welcome interface
    [w, screenRect, oldclut]=pton([],[],[],1); % note here should specify clut file
    Screen('BlendFunction',w,'GL_SRC_ALPHA','GL_ONE_MINUS_SRC_ALPHA');
    Screen('TextSize',w,30); Screen('TextFont',w,'Charcoal');
    sr_hor = round(screenRect(3)/2); sr_ver = round(screenRect(4)/2);
      
    %% show instruction
    Screen('DrawText',w,[int2str(total_trials),'  nTrials. Press space key to start the experiment'],sr_hor-300,sr_ver-180,0);
    Screen('DrawText',w,'Choose one of two motion directions',sr_hor-300,sr_ver-140,0); 
    Screen('DrawText',w,'Left, press "leftArrow"; Right, press "rightArrow"',sr_hor-300,sr_ver-100,0);
    Screen('DrawLines',w,cuexy1,2,0,[sr_hor sr_ver],1);
    Screen('Flip',w); % fresh
    getkeyresp('Space'); % press space to start
    Screen('Flip', w);
    FlushEvents('keyDown');
    
    %% prepare the movie make
    bps  = round(60*radius/scale_factor)*2;
    movieRect = [0,0,bps,bps];
    screenPatch = CenterRect(movieRect, screenRect);
     
    %% now start the main loop
    trial = 1;
    while trial <= total_trials
           
        t1 = GetSecs;
        
        %% use staircase to get current_t in this trial...
        curr_stair_index    = data( trial, 2);          %1-2,indicate staircase number
        time_sigma = curr_stair_t(curr_stair_index);    %current time matrix,contain t in this size,here we got how many frames
        if time_sigma >= upper_limit
            time_sigmaP = upper_limit;
        else
            time_sigmaP = time_sigma;
        end
        
        % derive temporal envelope
        [time_gauss, mvLength] = envelope( 0.5*time_sigmaP/1000, frameRate, which_envelope, amplitude);
        time_gauss = time_gauss/amplitude;
        
        %% calculate the moving direcion
        direction = data(trial,5); %
        switch direction
            case 1%left
                angle_patch = 0;
                corrKey = 'LeftArrow';
            case 2%right
                angle_patch = 180;
                corrKey = 'RightArrow';
        end
        %% ------------------------premake the movie before the trial----------------------------
        movie = createDriftGrating(bps, ...
            'orientation',orientation, ...
            'cpfov',cpfov, ...
            'temporal',time_gauss, ...
            'TFstep', TFstep, ...
            'mvLength', mvLength,...
            'windowPtr',w);
        
        %%  initiate trial
        % before stimulus prep
        t2 = GetSecs - t1;
        
        FlushEvents('keyDown');
        WaitSecs(1-t2);
        Screen('FillRect',w, background);
        Screen('Flip', w);
        
        % use dynamic fixation
        mm = 19;
        for i=0:4
            nn = mm-i*4;
            Screen('FrameOval', w,60,[sr_hor-nn, sr_ver-nn, sr_hor+nn, sr_ver+nn],2,2)
            Screen('Flip', w);
            WaitSecs(0.05);
        end
        Screen('FrameOval', w,60,[sr_hor-nn, sr_ver-nn, sr_hor+nn, sr_ver+nn],2,2)
        Screen('Flip', w);
        WaitSecs(0.5);
        
        % play the movie, onset of the stimlus
        priorityLevel=MaxPriority(w);Priority(priorityLevel);
        Screen('Flip',w);
        for i = 1:mvLength
            Screen('DrawTexture', w, movie.driftGratingMovie{i}, movieRect, screenPatch, angle_patch);
            Screen('Flip',w);
        end
        Screen('FillRect',w, background);
        Screen('Flip',w);
        Priority(0);
        
        %% get and analyze the response 
        rs_key = getkeyresp({'LeftArrow','RightArrow'});        
        ampS = 1;
        if strcmp(rs_key, corrKey)
            rs = 1;
            Snd('Play',sin((0:1000))*ampS);
            Snd('Wait');
        else
            rs=0;
        end
        data(trial, 6:8) = [time_sigmaP, KbName(rs_key), rs]; % Here time_sigmaP millisecs
        
        %% update staircase,here we update how many frames, not exact duration
        if rs == 1  % correct response
            if curr_up_downs( curr_stair_index, 2 ) == up_down_design(curr_stair_index, 2 ) -1
                curr_stair_t( curr_stair_index ) = 10^( log10( time_sigmaP ) - (up_down_step_in_log+sign(rand(1)-0.5)*0.01)); % note here we add a little bit jitter to avoid fixed path of staircases 
                curr_up_downs( curr_stair_index, 2 ) = 0;                
                curr_up_downs( curr_stair_index, 1 ) = 0;
            else
                curr_up_downs( curr_stair_index, 2 ) = curr_up_downs( curr_stair_index, 2 ) + 1 ;
            end
        else  % wrong response            
            if curr_up_downs( curr_stair_index, 1 ) == up_down_design(  curr_stair_index, 1 ) -1
                curr_stair_t( curr_stair_index ) = 10^( log10( time_sigmaP ) + (up_down_step_in_log+sign(rand(1)-0.5)*0.01));
                curr_up_downs( curr_stair_index, 1 ) = 0;                
                curr_up_downs( curr_stair_index, 2 ) = 0;                
            else
                curr_up_downs( curr_stair_index, 1 ) = curr_up_downs( curr_stair_index, 1 ) + 1 ;
            end
        end
        
        %% clear movie from memory in this trial
        for i = 1:mvLength
            Screen(movie.driftGratingMovie{i}, 'Close');
        end
        trial = trial+1;
    end % end main loop
    time = toc/60
    
    %% save data
    filename = strcat(subjInitials,'_compo_',num2str,'.mat');
    IsExist = exist(filename,'file');
    if IsExist
        error('data file name exists')
    end
    save(filename);
    
    %% clean up
    ptoff(oldclut);
catch errorName
    sca; % exit screens
    save errorName_debug;
    rethrow(errorName);
    ptoff(oldclut);
end


function restoreMonitor