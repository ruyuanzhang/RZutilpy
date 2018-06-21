def path(whichpath):

    '''
    path(whichpath):

    Return the path specified in 'whichpath'
    Hardcode common paths here, then call this function elsewhere to maximize
    flexibility.
    Possibilities:
    'code'        (common cvnlab code on Dropbox)
    'ppresults'   (cvnlab pre-processing results on Dropbox)
    'freesurfer'  (FreeSurfer subjects directory)
    'fmridata'    (fmridata directory on stone)
    'anatomicals' (anatomicals directory on stone)
    'workbench'   (location of HCP wb_command)
    eg: fsdir=sprintf('%s/%s',cvnpath('freesurfer'),subjectid)
       instead of hardcoding in every function
    Note: If you have /stone/ext1 followed by /home/stone-ext1, this ensures
    that you can access it from any machine, and if we ARE on stone, it
    will use the faster local route /stone/ext1


    Note:
        20180620 RZ create it. based on cvnpath.m
    '''
    from os.path import exists

    paths = {\
        'code':\
            [
            '/home/stone/generic/Dropbox/cvnlab/code',
            ],
        'commonmatlab':\
            [
            '/home/stone/software/commonmatlabcode',
            ],
        'ppresults':\
            [
            '/home/stone/generic/Dropbox/cvnlab/ppresults',
            ],
        'freesurfer':\
            [
            '/stone/ext1/freesurfer/subjects',
            '/home/stone-ext1/freesurfer/subjects'
            ],
        'fmridata':\
            [
            '/stone/ext1/fmridata',
            '/home/stone-ext1/fmridata'
            ],
        'anatomicals':\
            [
            '/stone/ext1/anatomicals',
            '/home/stone-ext1/anatomicals'
            ],
        'workbench':\
            [
            '/home/stone/software/workbench_v1.1.1/bin_rh_linux64',
            '/Applications/workbench/bin_macosx64'
            ]
    }

    p = [p for p in paths[whichpath] if exists(p)]
    if p:
        return p[0]  # we return the 1st valid path
    else:
        raise ValueError('No path found for {}'.format(whichpath))

