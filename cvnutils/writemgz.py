def writemgz(subjectid, name, vals, hemi, outputdir=None, surfsuffix=None):
    '''
    function cvnwritemgz(subjectid,name,vals,hemi,outputdir,surfsuffix)

    <subjectid> is like 'C0041' (can be 'fsaverage')
    <name> is a string, filename
    <vals> is a vector of values for the surface
    <hemi> is 'lh' or 'rh'
    <outputdir> (optional) is the directory to write the file to.
        Default is cvnpath('freesurfer')/<subjectid>/surf/
    <surfsuffix> (optional) is a suffix to tack onto <hemi>, e.g., 'DENSETRUNCpt'.
        Special case is 'orig' which is equivalent to ''.
        Default: 'orig'.

    Write a file like <hemi><surfsuffix>.<name>.mgz.


    # ======================== RZ notes =======================================
    Note that, unlike cvnwritemgz.m, we do not mangle the headerinformation (see code).
    This is due to inherent difference between nibabel and matlab MRIread.m
    history:
        20180714 RZ start to use pathlib object, <outputdir> now accept path-like object

    '''
    from RZutilpy.cvnpy import cvnpath
    from RZutilpy.system import makedirs
    import os
    import nibabel as nib

    # calc
    fsdir = (Path(cvnpath('freesurfer')) / subjectid).str

    # input
    outputdir = (Path(fsdir) / 'surf').str if outputdir is None else outputdir

    if surfsuffix is None:
        surfsuffix = 'orig'

    # prep
    makedirs(outputdir)

    # load template
    file0 = (Path(fsdir) / 'surf' / '{}.w-g.pct.mgh'.format(hemi)).str

    if not Path(file0).exists():  # fsaverage doesn't have the above file, so let's use this one:
        file0 = (Path(fsdir) / 'surf' / '{}.orig.avg.area.mgh'.format(hemi)).str

    fsmgh = nib.load(file0)

    # calc
    suffstr = '' if surfsuffix == 'orig' else surfsuffix

    file = (Path(outputdir) / f'{hemi}{suffstr}.{name}.mgz').str

    ## mangle the field, did this in cvnwritemgz but no need to here.
    # n = numel(vals);
    # # mangle
    # fsmgh.fspec = file;
    # fsmgh.vol = flatten(vals);
    # fsmgh.volsize = [1 n 1];
    # fsmgh.width = n;
    # fsmgh.nvoxels = n;

    # write
    nib.save(vals.flatten(), file, fsmgh)

