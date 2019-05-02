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
    from RZutilpy.cvnpy import cvnpath
    from RZutilpy.system import unix_wrapper
    from RZutilpy.imageprocess import makeimagestack3dfiles
    from RZutilpy.system import Path


    dir0 = (Path(cvnpath('anatomicals')) / subjectid).str
    fsdir = (Path(cvnpath('freesurfer')) / subjectid).str
    pp0 = (Path(cvnpath('ppresult')) / subjectid).str

    # find T2 NIFTI
    t2nifti = (Path(dir0) / 'T2average.nii.gz').str

    # find T1 NIFTI
    t1nifti = (Path(fsdir) / 'mri' / 'T1.nii.gz').str

    # define output file
    t2tot1nifti = (Path(fsdir) / 'mri' / 'T2alignedtoT1.nii.gz').str

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
    makeimagestack3dfiles(t1nifti, (Path(pp0) / 'T1T2alinment'/ 'T1').str, skips=(5, 5, 5), k=[1, 1, 0], wantnorm=1, addborder=1)
    makeimagestack3dfiles(t2tot1nifti, (Path(pp0) / 'T1T2alinment'/'T2').str, skips=(5, 5, 5), k=[1, 1, 0], wantnorm=1, addborder=1)




