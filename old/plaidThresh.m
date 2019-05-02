%% measure duration thresholds in components 
%% it's 2AFC task
%% to minimize practice effects, we used staircase to measure thresholds in pre/post tests

function plaidThresh(subject_initials,p,test_con)
%%
%clc;clear all;close all;
warning('off','MATLAB:dispatcher:InexactMatch');
KbName('UnifyKeyNames');
ListenChar(2);
% KEY Monitor Parameters
scale_factor   = 2.00;       % most important parameter - how many acrmin is one screen pixel? for SONY monitor at [1024 640] resolution, and 30.4in vieving distance, use scale_factor=2
frame_rate     = 360;        % 
linearize 	   = 1;          % whether monitor is linearized. if=1, program will look for "MyGammaTable"

%% --------file name------------------- 
filename = strcat(subject_initials,'_plaid_',num2str(test_con),'.mat');

IsExist = exist(filename,'file');
if IsExist
    error('data file name exists')
end



%%-----load parameters-------------------------------------------
orientation            = p.orientation;
speed                  = p.speed;        %deg/sec
radius                 = p.radius;
trials                 = p.trials;       %how many trials/staircase       
train_condition        = p.train_condition;

contrast               = 100; 


%--------STIMULI parameters-------------------------------             
SF                     = 1;        %cycles/deg
TF 					   = speed*SF;


spatial_envelope       = 2;        %0 = disk, 1 = Gabor patch, 2 = raised cosine envelope
which_envelope 	       = 2;
background             = 126;      %background intensity, in gray scale untis
white                  = background*2;
n_alternatives         = 2;



%-------other parameters----------------
l = 7;
ww = 4;
%---------------------------------------
cuexy1=[3 40 35 40 35 40 ;
        0 0 -5 0 5 0];
cuexy1=[cuexy1 -cuexy1];% for, orientation==0   
cuexy4=[cuexy1(2,:);cuexy1(1,:)];
cuexy4=[cuexy4 -cuexy4];

   
cuexy=[3 40 25 40 33 40;
       3 40 33 40 25 40];
cuexy2=[cuexy -cuexy]; %for orientation=45
cuexy3=[-cuexy(1,:) cuexy(1,:);cuexy(2,:) -cuexy(2,:)];

%

%initialize staircase
upper_limit              = 0.4;      %minisec
start_point              = [0.11 0.1];
stair_consecutive        = 1;        %1 means conventional staircase design. n consecutive up is up. 0 mean every n up is up. we can set different percentage correct by choosing different design.
up_down_step_in_log      = 0.1;      %step size log unit
%trials                   = 80;       %number of trials per staircase
n_alternatives           = 2;        

if stair_consecutive == 1
    up_down_design = [ 1,2; 1,3; ];%%% [up, down].  %because 2AFC, we use 2/1 and 3/1 staircases
else
    up_down_design = [ 2,1; 1,2; 1,7 ];%%% [up, down].
end

curr_up_downs  = zeros( size( up_down_design) );
curr_stair_t   = start_point ;



H_ecc_fix       = 0;      H_ecc_fix  = H_ecc_fix*60/scale_factor;
V_ecc_fix       = 0;      V_ecc_fix  = V_ecc_fix*60/scale_factor;
H_ecc_stim      = 0;      H_ecc_stim = round(H_ecc_stim*60/scale_factor);
V_ecc_stim      = 0;      V_ecc_stim = round(V_ecc_stim*60/scale_factor);


%data structure

total_trials    =trials*size(up_down_design,1);  %per block
data            =zeros(total_trials,8);% trial number,Quest number,contrast,size,duration,direction,choice,correct
data(:,1)       =(1:total_trials)';
data(:,3)       =contrast;
data(:,4)       =radius;

staircase_list =sort(repmat((1:size(up_down_design,1))',trials,1));
direction_list =repmat((1:2)',total_trials/2,1);  
[staircase_list, index]=Shuffle(staircase_list);direction_list=direction_list(index);
data(:,2)=staircase_list;data(:,6)=direction_list;
  
   
    
try
    %open Screen windows,
    Screen('Preference', 'SkipSyncTests', 1);
    oldVisualDebugLevel = Screen('Preference', 'VisualDebugLevel', 3);
    oldSupressAllWarnings = Screen('Preference', 'SuppressAllWarnings', 1);
    screens=Screen('Screens');
    screenNumber=max(screens);
    %w=Screen('OpenWindow',screenNumber,0,[],8,2);
    w=Screen('OpenWindow',screenNumber,0,[],[],2);
    
    screen_rect = Screen('Rect',w);
    if linearize
        screen_clut = [linspace(0,1,256)' linspace(0,1,256)' linspace(0,1,256)'];
        Screen('LoadNormalizedGammaTable',screenNumber,screen_clut);
    end
    Screen('FillRect',w, background);Screen('Flip', w);Screen('FillRect',w, background);
    Screen('TextSize',w,30);Screen('TextFont',w,'Charcoal');
    Screen('BlendFunction',w,'GL_SRC_ALPHA','GL_ONE_MINUS_SRC_ALPHA');
    
    sr_hor = round(screen_rect(3)/2); sr_ver = round(screen_rect(4)/2);
    
    
    % MAIN LOOP
    %HideCursor;
    tic; skip_first = 1;trial = 1;
    %Screen(w,'DrawLine',0,sr_hor-l+H_ecc_fix,sr_ver+V_ecc_fix,sr_hor+l+H_ecc_fix,sr_ver+V_ecc_fix,ww);
    %Screen(w,'DrawLine',0,sr_hor+H_ecc_fix,sr_ver-l+V_ecc_fix,sr_hor+H_ecc_fix,sr_ver+l+V_ecc_fix,ww);
    %     Screen('DrawText',w,['KEEP YOUR EYES ON THE FIXATION POINT above!'],sr_hor-300,sr_ver+50,0);
    %     Screen('DrawText',w,['press LEFT arrow for LEFTWARD motion'],sr_hor-300,sr_ver+300,0);
    %     Screen('DrawText',w,['press RIGHT arrow for RIGHTWARD motion'],sr_hor-300,sr_ver+350,0);
    %     Screen('DrawText',w,['press SPACE BAR to inititate each trial'],sr_hor-300,sr_ver+250,0);
    
    Screen('DrawText',w,[int2str(total_trials),'  trials. Press space key to start the experiment'],sr_hor-300,sr_ver-180,0);
    Screen('DrawText',w,'Choose one of two motion directions',sr_hor-300,sr_ver-140,0);
    if orientation==0
        Screen('DrawText',w,'Left, press "leftArrow"; Right, press "rightArrow"',sr_hor-300,sr_ver-100,0);
        Screen('DrawLines',w,cuexy1,2,0,[sr_hor sr_ver],1);
    elseif orientation==90
        Screen('DrawText',w,'Up, press "UpArrow"; Down, press "DownArrow"',sr_hor-300,sr_ver-100,0);
        Screen('DrawLines',w,cuexy4,2,0,[sr_hor sr_ver],1)
    elseif orientation == 45
        Screen('DrawText',w,'Upleft, press "4"; Downright, press "2"',sr_hor-300,sr_ver-100,0);
        Screen('DrawLines',w,cuexy2,2,0,[sr_hor sr_ver],1);
    elseif orientation == -45
        Screen('DrawText',w,'Upright, press "5";Downleft, press "1"',sr_hor-300,sr_ver-100,0);
        Screen('DrawLines',w,cuexy3,2,0,[sr_hor sr_ver],1);
    end

    Screen('Flip',w);
    KbWait(-1);
    
    GetChar;
    Screen(w,'DrawLine',0,sr_hor-l+H_ecc_fix,sr_ver+V_ecc_fix,sr_hor+l+H_ecc_fix,sr_ver+V_ecc_fix,ww);
    Screen(w,'DrawLine',0,sr_hor+H_ecc_fix,sr_ver-l+V_ecc_fix,sr_hor+H_ecc_fix,sr_ver+l+V_ecc_fix,ww);
    Screen('Flip', w);
    
 
    FlushEvents('keyDown');
    
    
    
    %housekeeping stuff for drift grating
    stimulus_radius  = round(60*radius/scale_factor);
    TFstep = (2*pi*TF)/frame_rate;
    f=(SF*scale_factor/60)*2*pi;
    orient=0*pi/180;
    a=cos(orient)*f; b=sin(orient)*f;
    q1 = 1; q2 = 1;
    amplitude = background*contrast/100;
    
    
    % make the spatial envelope
    [x,y]=meshgrid(-stimulus_radius:stimulus_radius,-stimulus_radius:stimulus_radius);
    bps = (stimulus_radius)*2+1;
    circle=((stimulus_radius)^2-(x.^2+y.^2));
    for i=1:bps;
        for j =1:bps;
            if circle(i,j) < 0; circle(i,j) = 0;
            else
                circle(i,j) = 1;
            end;
        end;
    end;
    if spatial_envelope == 1
        circle = (exp(-(((x)/(sqrt(2)*Gaussian_stdev/2)).^2)-((y/(sqrt(2)*Gaussian_stdev/2)).^2)).*circle);
    elseif spatial_envelope == 2
        R = (sqrt(x.^2 + y.^2) + eps).*circle;R = R/max(max(R));
        cos2D = (cos(R*pi)+1)/2;circle = (cos2D.*circle);
    end
    
    % create stimulus rectangle_patchs
    movie_rect = [0,0,bps,bps];
    scr_left_middle = fix(screen_rect(3)/2)-round(bps/2);
    scr_top = fix(screen_rect(4)/2)-round(bps/2);
    screen_rect_middle = movie_rect + [scr_left_middle, scr_top+V_ecc_fix, scr_left_middle, scr_top+V_ecc_fix];
    screen_patch = screen_rect_middle+[H_ecc_stim,V_ecc_stim,H_ecc_stim,V_ecc_stim];
    
    
    while trial <= total_trials
        
        
        
        t1 = GetSecs;
   
        
      
        %%%%%%use staircase to get current_t here...
        curr_stair_index    = data( trial, 2 );          %1-2,indicate staircase number
        time_sigma = curr_stair_t(curr_stair_index );    %current time matrix,contain t in this size,here we got how many frames

        
        
        if time_sigma >= upper_limit;
            time_sigmaP = upper_limit;
            limit = 1;
        else
            time_sigmaP = time_sigma;
            limit = 0;
        end
        
        
        
        amplitude=background*contrast/100;
        
        %time_sigmaP=0.005;
        [time_gauss,mv_length] = envelope( 0.5*time_sigmaP, frame_rate, which_envelope, amplitude );
        time_gauss = time_gauss/amplitude;
        
        mv_length
        
       
        %% calculate the moving direcion
        direction = data(trial,6); %
        if orientation==0 %left/right
            switch direction
                case 1%left
                    angle_patch = -45;
                    corrKey = KbName('LeftArrow');	incorrKey = KbName('RightArrow');
                case 2%right
                    angle_patch = 135;
                    corrKey = KbName('RightArrow');	incorrKey = KbName('LeftArrow');
            end
           
        elseif orientation==90
            switch direction
                case 1%up
                    angle_patch = 45;
                    corrKey = KbName('UpArrow');	incorrKey = KbName('DownArrow');
                case 2%down
                    angle_patch = 225;
                    corrKey = KbName('DownArrow');	incorrKey = KbName('UpArrow');
            end
            
        elseif orientation==45
            switch direction
                case 1%upleft
                    angle_patch = 0;
                    corrKey = KbName('4');	incorrKey = KbName('2'); 
                case 2%downright
                    angle_patch = 180;
                    corrKey = KbName('2');	incorrKey = KbName('4'); 
            end
            
        elseif orientation==-45
            switch direction
                case 1%downleft
                    angle_patch = -90;
                    corrKey = KbName('1');	incorrKey = KbName('5'); 
                case 2%upright
                    angle_patch = 90;
                    corrKey = KbName('5');	incorrKey = KbName('1'); 
            end
           
        end
        
        
        %% ------------------------make the movie----------------------------
        %make the movie
        motion_step(1) = rand*2*pi;
        for i=2:mv_length;
            motion_step(i) = motion_step(i-1)+TFstep;
        end

        for i = 1:mv_length;
            grating1=round(((sin(a*x+b*y+motion_step(i)).*circle*amplitude*time_gauss(i))+background));
            grating2=grating1';
            movie{i}=(grating1+grating2)/2;
            %movie{i}=grating1;
        end
        frame = zeros(bps,bps,3);
        for i = 1:ceil(mv_length/3)
            for j=1:3
                if ((i-1)*3+j)>mv_length
                    %frame(:,:,j) = ones(bps)*background;
                    switch j
                        case 1
                            frame(:,:,3) = ones(bps)*background;
                        case 2
                            frame(:,:,1) = ones(bps)*background;
                        case 3
                            frame(:,:,2) = ones(bps)*background;
                    end
                else
                    switch j
                        case 1
                            frame(:,:,3) = movie{(i-1)*3+j};
                        case 2
                            frame(:,:,1) = movie{(i-1)*3+j};
                        case 3
                            frame(:,:,2) = movie{(i-1)*3+j};
                    end
                end
            end
            movie_play{i} = Screen('MakeTexture',w,frame);
        end
        
        %done with the movie

        

       
        
        %%  initiate trial
        t2 = GetSecs - t1;

        FlushEvents('keyDown');
        WaitSecs(1-t2);

        Screen('FillRect',w, background);
        Screen('Flip', w);
        mm = 19;
        for i=0:4
            nn = mm-i*4;
            Screen('FrameOval', w,60,[sr_hor-nn, sr_ver-nn+V_ecc_fix, sr_hor+nn, sr_ver+nn+V_ecc_fix],2,2)
            Screen('Flip', w);
            WaitSecs(0.05);
        end
        Screen('FrameOval', w,60,[sr_hor-nn, sr_ver-nn+V_ecc_fix, sr_hor+nn, sr_ver+nn+V_ecc_fix],2,2)
        Screen('Flip', w);
        WaitSecs(0.36);
 
        Screen('FillRect',w, background);
        Screen('Flip', w);
        WaitSecs(0.3);
        

        % play the movie
        priorityLevel=MaxPriority(w);Priority(priorityLevel);
        blah=GetSecs;
        Screen('Flip',w);
        
        for i = 1:ceil(mv_length/3);
            %angle_patch =0;
            Screen('DrawTexture', w, movie_play{i}, movie_rect, screen_patch, angle_patch);
            Screen('Flip',w);
        end;
        Screen('FillRect',w, background);
        Screen('Flip',w);
        
        
        Priority(0);
        
        % get the response && Update QUEST
        FlushEvents('keyDown');
        while (1);
            [keyIsDown,secs,keyCode] = KbCheck(-1);
            if keyIsDown;
                if keyCode(corrKey) || keyCode(incorrKey) 
                    break;
                else
                    keyIsDown = 0;
                end;
            end
        end
        Screen('FillRect',w, background);
        vbl=Screen('Flip', w);
        ampS = 1;
        if keyCode(corrKey);
            rs = 1;
            Snd('Play',sin((0:1000))*ampS);
            Snd('Wait');
        else
            rs=0;
        end
          
        rs_key = find(keyCode == 1);
        data( trial, 5:8 ) = [time_sigmaP, direction, rs_key, rs]; %here time_sigmaP is number of frames
        FlushEvents('keyDown');
        
        
        %update staircase,here we update how many frames, not exact

        if rs == 1
           
            if curr_up_downs( curr_stair_index, 2 ) == up_down_design(  curr_stair_index, 2 ) -1
                curr_stair_t( curr_stair_index ) = 10^( log10( time_sigmaP ) - (up_down_step_in_log+sign(rand(1)-0.5)*0.01));
                curr_up_downs( curr_stair_index, 2 ) = 0;
       
                curr_up_downs( curr_stair_index, 1 ) = 0;  
            else
                curr_up_downs( curr_stair_index, 2 ) = curr_up_downs( curr_stair_index, 2 ) + 1 ;
            end
            
        else
            
            if curr_up_downs( curr_stair_index, 1 ) == up_down_design(  curr_stair_index, 1 ) -1
                curr_stair_t( curr_stair_index ) = 10^( log10( time_sigmaP ) + (up_down_step_in_log+sign(rand(1)-0.5)*0.01));
                curr_up_downs( curr_stair_index, 1 ) = 0;
                
                curr_up_downs( curr_stair_index, 2 ) = 0;
                
            else
                curr_up_downs( curr_stair_index, 1 ) = curr_up_downs( curr_stair_index, 1 ) + 1 ;
            end
        end
        
        
        
        FlushEvents('keyDown');
        % Close movies
        for i = 1:ceil(mv_length/3);
            % if time_gauss(i) ~= amplitude;
            Screen(movie_play{i}, 'Close');
            % end
        end
        clear movie motion_step;
        
        trial = trial+1;
    end
    
    
    
    save(filename);

    if trials ==80
    %set a break
    %break countdown (added by RZ 10/15/2014)
    JustBreak(w,60,-1);
    Snd('Play',sin((1:1000)));
    WaitSecs(.5)
    Snd('Play',sin((1:1000)));
    WaitSecs(.5)
    Snd('Play',sin((1:1000)));
    end


    

    screen_clut = [0:255; 0:255; 0:255]'./(255);
    Screen('LoadNormalizedGammaTable',screenNumber,screen_clut);
    Screen('CloseAll');
    Screen('Preference', 'VisualDebugLevel', oldVisualDebugLevel);
    Screen('Preference', 'SuppressAllWarnings', oldSupressAllWarnings);
    ListenChar(1);
catch
    ListenChar(1);
    ddd = lasterror;
    ddd.message
    ddd.stack(1,1).line
    psychrethrow(lasterror);
    screen_clut = [0:255; 0:255; 0:255]'./(255);
    Screen('LoadNormalizedGammaTable',screenNumber,screen_clut);
    Screen('CloseAll');
    Screen('Preference', 'VisualDebugLevel', oldVisualDebugLevel);
    Screen('Preference', 'SuppressAllWarnings', oldSupressAllWarnings);
    Priority(0);
end %try..catch..
time = toc/60;
end


%%