%% Experiement 2



%%
clc;clear all;close all;
warning('off','MATLAB:dispatcher:InexactMatch');
ListenChar(2);


%% --------change parameters here-------------------
subject_initials      ='RZ';
exp_day               = 7;
p.train_condition     = 1; %1,left/right; 2, up/down


%% -----exp parameters----
p.speed               = 4;
p.contrast            = 50;
p.radius              = 8;

%% --------------------------------------------------
task_order = Shuffle(1:6);  %shuffle the condition

if exp_day == 1 % practice
    subject_initials=[subject_initials '_practice'];
    p.trials = 30;
    for i=1:6
        switch task_order(i)
            case 1 %component at trained direction
                if p.train_condition == 1 %left/right training
                    p.orientation=0;
                elseif p.train_condition == 2
                    p.orientation=90;
                end
                p.conditionMarker='Large_HC_Compo_trainedDirect';
                compoThresh(subject_initials,p,1);
            case 2
                if p.train_condition == 1 %up/down training
                    p.orientation=90;
                elseif p.train_condition == 2
                    p.orientation=0;
                end
                p.conditionMarker='Large_HC_Compo_untrainedDirect';
                compoThresh(subject_initials,p,2);
            case 3
                if p.train_condition == 1 
                    p.orientation=0;
                elseif p.train_condition == 2
                    p.orientation=90;
                end
                p.conditionMarker='Large_HC_plaid_trainedDirect';
                plaidThresh(subject_initials,p,1);
            case 4
                if p.train_condition == 1 
                    p.orientation=45;
                elseif p.train_condition == 2
                    p.orientation=-45;
                end
                p.conditionMarker='Large_HC_plaid_untrainedDirect';
                plaidThresh(subject_initials,p,2);
            case 5
                if p.train_condition == 1 %
                    p.orientation=0;
                    p.radius = 1;     %small size
                elseif p.train_condition == 2
                    p.orientation=90;
                    p.radius = 1;      
                end
                p.conditionMarker='small_HC_compo_trainedDirect';
                compoThresh(subject_initials,p,3);
                p.radius = 8;%rest to large
            case 6
                if p.train_condition == 1 
                    p.orientation=0;
                    p.contrast = 2;     %low contrast
                elseif p.train_condition == 2
                    p.orientation=90;
                    p.contrast = 2;     %
                end
                p.conditionMarker='large_LC_compo_trainedDirect';
                compoThresh(subject_initials,p,4);
                p.contrast = 50;%rest to high contrasts
        end 
    end
elseif exp_day == 2 %pretest
    subject_initials=[subject_initials '_pre'];
    p.trials = 80;
    for i=1:6
        switch task_order(i)
            case 1 %component at trained direction
                if p.train_condition == 1 %left/right training
                    p.orientation=0;
                elseif p.train_condition == 2
                    p.orientation=90;
                end
                p.conditionMarker='Large_HC_Compo_trainedDirect';
                compoThresh(subject_initials,p,1);
            case 2
                if p.train_condition == 1 %up/down training
                    p.orientation=90;
                elseif p.train_condition == 2
                    p.orientation=0;
                end
                p.conditionMarker='Large_HC_Compo_untrainedDirect';
                compoThresh(subject_initials,p,2);
            case 3
                if p.train_condition == 1 
                    p.orientation=0;
                elseif p.train_condition == 2
                    p.orientation=90;
                end
                p.conditionMarker='Large_HC_plaid_trainedDirect';
                plaidThresh(subject_initials,p,1);
            case 4
                if p.train_condition == 1 
                    p.orientation=45;
                elseif p.train_condition == 2
                    p.orientation=-45;
                end
                p.conditionMarker='Large_HC_plaid_untrainedDirect';
                plaidThresh(subject_initials,p,2);
            case 5
                if p.train_condition == 1 %
                    p.orientation=0;
                    p.radius = 1;     %small size
                elseif p.train_condition == 2
                    p.orientation=90;
                    p.radius = 1;      
                end
                p.conditionMarker='small_HC_compo_trainedDirect';
                compoThresh(subject_initials,p,3);
                p.radius = 8;%rest to large
            case 6
                if p.train_condition == 1 
                    p.orientation=0;
                    p.contrast = 2;     %low contrast
                elseif p.train_condition == 2
                    p.orientation=90;
                    p.contrast = 2;     %
                end
                p.conditionMarker='large_LC_compo_trainedDirect';
                compoThresh(subject_initials,p,4);
                p.contrast = 50;%rest to high contrasts
        end 
    end
elseif exp_day >2 && exp_day<7
    compoTrain
elseif exp_day==7
    subject_initials=[subject_initials '_post'];
    p.trials = 80;
    for i=1:6
        switch task_order(i)
            case 1 %component at trained direction
                if p.train_condition == 1 %left/right training
                    p.orientation=0;
                elseif p.train_condition == 2
                    p.orientation=90;
                end
                p.conditionMarker='Large_HC_Compo_trainedDirect';
                compoThresh(subject_initials,p,1);
            case 2
                if p.train_condition == 1 %up/down training
                    p.orientation=90;
                elseif p.train_condition == 2
                    p.orientation=0;
                end
                p.conditionMarker='Large_HC_Compo_untrainedDirect';
                compoThresh(subject_initials,p,2);
            case 3
                if p.train_condition == 1 
                    p.orientation=0;
                elseif p.train_condition == 2
                    p.orientation=90;
                end
                p.conditionMarker='Large_HC_plaid_trainedDirect';
                plaidThresh(subject_initials,p,1);
            case 4
                if p.train_condition == 1 
                    p.orientation=45;
                elseif p.train_condition == 2
                    p.orientation=-45;
                end
                p.conditionMarker='Large_HC_plaid_untrainedDirect';
                plaidThresh(subject_initials,p,2);
            case 5
                if p.train_condition == 1 %
                    p.orientation=0;
                    p.radius = 1;     %small size
                elseif p.train_condition == 2
                    p.orientation=90;
                    p.radius = 1;      
                end
                p.conditionMarker='small_HC_compo_trainedDirect';
                compoThresh(subject_initials,p,3);
                p.radius = 8;%rest to large
            case 6
                if p.train_condition == 1 
                    p.orientation=0;
                    p.contrast = 2;     %low contrast
                elseif p.train_condition == 2
                    p.orientation=90;
                    p.contrast = 2;     %
                end
                p.conditionMarker='large_LC_compo_trainedDirect';
                compoThresh(subject_initials,p,4);
                p.contrast = 50;%rest to high contrasts
        end 
    end
end
