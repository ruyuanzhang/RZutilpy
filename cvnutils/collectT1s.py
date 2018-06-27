def collectT1s(subjectid,dataloc, gradfile=None, str0='T1w', wantskip=True):
    '''
    def collectT1s(subjectid,dataloc,gradfile,str0,wantskip):

    <subjectid> a str, like 'C0001'
    <dataloc> is a scan directory like '/home/stone-ext1/fmridata/20151014-ST001-wynn,subject1'
        or a list of scan directories
    <gradfile>  is gradunwarp's scanner or coeff file (e.g. 'prisma').
        Default is None which means do not perform gradunwarp.
    <str0> a str is the filename match thing. Default: 'T1w'.
    <wantskip> boolean, is whether to treat as pairs and use the second of each pair.
        (The idea is that the second of each pair might be homogeneity-corrected.)
        Default: True.

    Within the specified scan directories (in the order as given),
    find all of the T1 (or whatever) DICOM directories, and if <wantskip>,
    ignoring the 1st of each pair and keeping the 2nd of each pair.
    Then convert these DICOM directories to NIFTI files.
    If <gradfile> is specified, we additionally run fslreorient2std
    and gradunwarp.

    We return a cell vector of the final NIFTI filenames,
    preserving the order. Note that filenames will be different
    depending on whether <gradfile> is used.

    See code for specific assumptions.
    we use muliprocessin.Pool for speed-ups!

    To do:
        - consider using nipype wrapper of dcm2nii??
        -

    history:
        - 20180620 RZ created it based on cvncollectT1s.m
    '''
    from RZutilpy.cvnpy import cvnpath
    from RZutilpy.system import makedirs, unix_wrapper
    from RZutilpy.rzio import matchfiles
    import re
    from multiprocessing import Pool  # note 1st letter uppercase
    from os.path import join

    dir0 = join(cvnpath('anatomicals'), subjectid)

    # make subject anatomical directory
    assert makedirs(dir0)

    # massage
    if ~isinstance(dataloc, list):
        dataloc = [dataloc]

    # figure out T1 DICOM directories [ASSUME THAT THERE ARE AN EVEN NUMBER OF DIRECTORIES IN EACH SCAN SESSION]
    t1files = []
    for p in dataloc:
        t1files0 = matchfiles(join(p, 'dicom','*%s*' % str0))
        if wantskip:
            assert len(t1files0) % 2 == 0
            t1files0 = t1files0[1::2]
        # collect them up
        t1files = t1files + t1files0

    # convert dicoms to NIFTIS and get the filenames
    files = []
    for p in t1files:
        result = unix_wrapper('dcm2nii -o %s -r N -x N %s' % (dir0, p))
        temp = re.findall(r'GZip[.]*(\w+.nii.gz)', result)
        files.append(dir0 + '/' + temp[0])


    # perform grandunwarp
    if grandfile:
        # run Keith's fslreorient2std on each
        [unix_wrapper('fslreorient2std_inplace %s' % p) for p in files]

        # then do grandunwarp
        # extract filename and give new files
        assert all([p[-7:]=='.nii.gz' for p in files])
        file0 = [p[:-7] for p in files]
        newfiles = [p + '_gradunwarped.nii.gz' for p in file0]

        # do the grandunwarp
        def gradunwarp(filename):
            unix_wrapper('gradunwarp -w %s_warp.nii.gz -m %s_mask.nii.gz %s.nii.gz %s_gradunwarped.nii.gz %s' \
                % (filename,filename,filename,filename, gradfile))

        if __name__ == '__main__':
            with Pool(12) as p:
                p.imap_unordered(gradunwarp, file0)

        files = list(newfiles)

    return files








