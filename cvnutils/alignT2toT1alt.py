def alignT2toT1alt(subjectid, wantmi=True):
    '''
    alignT2toT1alt(subjectid, wantmi=True):

    <subjectid> is like 'C0001'
    <wantmi> is whether to use mutual information as the metric

    Load T2 volume from T2average.nii.gz. Register to the FreeSurfer T1.nii.gz volume.
    To perform the registration, we use flirt, using a rigid-body transformation and
    sinc interpolation.  The output is a file called T2alignedtoT1.nii.gz written to
    the FreeSurfer mri directory.

    See code for assumptions.
    '''
    from RZutilpy.cvnpy import path
    from RZutilpy.system import unix_wrapper
    from RZutilpy.imageprocess import makeimagestack3dfiles

    from os import path

    dir0 = path.join(path('anatomicals'), subjectid)
    fsdir = path.join(path('freesurfer'), subjectid)
    pp0 = path.join(path('ppresult'), subjectid)

    # find T2 NIFTI
    t2nifti = path.join(dir0, 'T2average.nii.gz')

    # find T1 NIFTI
    t1nifti = path.join(fsdir, 'mri', 'T1.nii.gz')

    # define output file
    t2tot1nifti = path.join(fsdir, 'mri', 'T2alignedtoT1.nii.gz')

    # call flirt to perform the alignment
    if wantmi:
        extrastr = ['-cost', 'mutualinfo', '-searchcost', 'mutualinfo']
    else:
        extrastr = []

    cmd = ['flirt', '-v',\
    '-in', t2nifti,\
    '-ref', t1nifti,\
    '-out', t2tot1nifti,\
    ' -interp', 'sinc',\
    '-dof', '6',\
    ] + extrastr  # note that we add extrastr here
    # do it
    unix_wrapper(cmd)

    # inspect the results
    makeimagestack3dfiles(t1nifti, os.join(pp0, 'T1T2alinment', 'T1'), skips=(5, 5, 5), k=[1, 1, 0], wantnorm=1, addborder=1)
    makeimagestack3dfiles(t2tot1nifti, os.join(pp0, 'T1T2alinment', 'T2'), skips=(5, 5, 5), k=[1, 1, 0], wantnorm=1, addborder=1)




