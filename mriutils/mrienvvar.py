def mrienviron(softwarename, **kwargs):
    '''
    <softwarename>: a str, currently support
        'freesurfer', 'fsl', 'afni'
    <kwargs>: keyword arguments to CHANGE environment variable

    update all environment variables associated with a mri software. If no kwargs
    return a dict <mrienviron> of unchanged environment variables. If the environment vars
    have not been set in os.environ, we return it as none

    If kwargs are supplied
    we update environment variable. Note that for each software we only allow a few
    valid environment vars. If invalid keys of environ vars are supplied, we report error.
    See codes for the allowed environ vars for each software.

    Example:

    fsenvironvars = rz.mri.mrienvvar('freesurfer')
    fsenvironvars = rz.mri.mrienvvar('fsl')
    fsenvironvars = rz.mri.mrienvvar('freesurfer', 'MNI_DIR', '/User/home')

    To do:
    1. handle afni later

    '''
    import os
    from RZutilpy.program import updatedict
    assert isinstance(softwarename, str), 'Input softwarename should be a str, e.g.,"freesurfer"'

    softwarename = softwarename.lower()
    assert softwarename in ['freesurfer', 'fsl', 'afni'], 'Input softwarename is wrong!'

    if softwarename == 'freesurfer':
        # environment variables for freesurfer are derived below
        #  https://surfer.nmr.mgh.harvard.edu/fswiki/SetupConfiguration_Linux

        # default environ vars dict
        default_environvars = {\
        'FREESURFER_HOME':None,\
        'FSFAST_HOME':None,\
        'FSF_OUTPUT_FORMAT':None,\
        'SUBJECTS_DIR':None,\
        'MNI_DIR':None}

    elif softwarename == 'fsl':
        default_environvars = {'FSLDIR':None}

    elif softwarename == 'afni':
        default_environvars={} # not sure how afni handle this..

    # check all keys in kwargs all also in freesurfer_environvars, otherwise raise error
    if not all([k in default_environvars.keys() for k in kwargs.keys()]):
        raise KeyError('environ vars "{}" in kwargs are not allowed for {}'.format(\
            ', '.join([k for k in kwargs.keys() if k not in default_environvars.keys()]), softwarename))

    # update environ from kwargs
    os.environ.update(kwargs)
    # update environvars based os.environ
    return updatedict(dict(os.environ), default_environvars, mode='extract')



