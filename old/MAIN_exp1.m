%% control program for pretest and posttest



%%
clc;clear all;close all;
warning('off','MATLAB:dispatcher:InexactMatch');
ListenChar(2);


%% --------change parameters here-------------------
subject_initials      ='test';
exp_day               =1;
p.train_condition     =1; %1,left/right; 2, up/down



%% --------------------------------------------------
task_order = Shuffle(1:6);  %shuffle the condition

if exp_day == 1 % practice
    subject_initials=[subject_initials '_practice'];
    p.trials = 30;
    for i=1:6
        %task_order(1)=3;
        switch task_order(i)
            case 1 %plaid at trained direction
                p.orientation = 0;
                p.speed       = 4;
                plaidThresh(subject_initials,p);
            case 2
                p.orientation = 90;
                p.speed       = 4;
                plaidThresh(subject_initials,p);
            case 3
                p.orientation = -45;
                p.speed       = 4;
                compoThresh(subject_initials,p);
            case 4
                p.orientation = 45;
                p.speed       = 4;
                compoThresh(subject_initials,p);                
            case 5
                if p.train_condition == 1 %left/right training
                    p.orientation=0;
                    p.speed = 4;     %component speed
                elseif p.train_condition == 2
                    p.orientation=90;
                    p.speed = 4;     %component speed
                end
                compoThresh(subject_initials,p);
            case 6
                if p.train_condition == 1 %left/right training
                    p.orientation=0;
                    p.speed = 5.66;    %plaid speed
                elseif p.train_condition == 2
                    p.orientation=90;
                    p.speed = 5.66;     %plaid speed
                end
                compoThresh(subject_initials,p);
        end 
    end
elseif exp_day == 2 %pretest
    subject_initials=[subject_initials '_pre'];
    p.trials = 80;
    for i=1:6
        switch task_order(i)
            case 1 %plaid at trained direction
                p.orientation = 0;
                p.speed       = 4;
                plaidThresh(subject_initials,p);
            case 2
                p.orientation = 90;
                p.speed       = 4;
                plaidThresh(subject_initials,p);
            case 3
                p.orientation = -45;
                p.speed       = 4;
                compoThresh(subject_initials,p);
            case 4
                p.orientation = 45;
                p.speed       = 4;
                compoThresh(subject_initials,p);                
            case 5
                if p.train_condition == 1 %left/right training
                    p.orientation = 0;
                    p.speed = 4;     %component speed
                elseif p.train_condition == 2
                    p.orientation = 90;
                    p.speed = 4;     %component speed
                end
                compoThresh(subject_initials,p);
            case 6
                if p.train_condition == 1 %left/right training
                    p.orientation = 0;
                    p.speed = 5.66;     %pattern speed
                elseif p.train_condition == 2
                    p.orientation = 90;
                    p.speed = 5.66;     %pattern speed
                end
                compoThresh(subject_initials,p);
        end
        
    end
elseif exp_day >2 && exp_day<7
    plaidsTrain
elseif exp_day==7
    subject_initials=[subject_initials '_post'];
    p.trials = 80;
    for i=1:6
        switch task_order(i)
            case 1 %plaid at trained direction
                p.orientation = 0;
                p.speed       = 4;
                plaidThresh(subject_initials,p);
            case 2
                p.orientation = 90;
                p.speed       = 4;
                plaidThresh(subject_initials,p);
            case 3
                p.orientation = -45;
                p.speed       = 4;
                compoThresh(subject_initials,p);
            case 4
                p.orientation = 45;
                p.speed       = 4;
                compoThresh(subject_initials,p);                
            case 5
                if p.train_condition == 1 %left/right training
                    p.orientation=0;
                    p.speed = 4;     %component speed
                elseif p.train_condition == 2
                    p.orientation=90;
                    p.speed = 4;     %component speed
                end
                compoThresh(subject_initials,p);
            case 6
                if p.train_condition == 1 %left/right training
                    p.orientation=0;
                    p.speed = 5.66;     %component speed
                elseif p.train_condition == 2
                    p.orientation=90;
                    p.speed = 5.66;     %component speed
                end
                compoThresh(subject_initials,p);
        end
    end
end
