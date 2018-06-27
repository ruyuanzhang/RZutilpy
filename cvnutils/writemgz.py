def writemgz(subjectid, name, vals, hemi, outputdir=None, surfsuffix=None):
    '''
    function cvnwritemgz(subjectid,name,vals,hemi,outputdir,surfsuffix)

    <subjectid> is like 'C0041' (can be 'fsaverage')
    <name> is a string
    <vals> is a vector of values for the surface
    <hemi> is 'lh' or 'rh'
    <outputdir> (optional) is the directory to write the file to.
    Default is cvnpath('freesurfer')/<subjectid>/surf/
    <surfsuffix> (optional) is a suffix to tack onto <hemi>, e.g., 'DENSETRUNCpt'.
    Special case is 'orig' which is equivalent to ''.
    Default: 'orig'.

    Write a file like <hemi><surfsuffix>.<name>.mgz.

    Note that, unlike cvnwritemgz.m, we do not mangle the headerinformation (see code).
    This is due to inherent difference between nibabel and matlab MRIread.m

    '''
    from RZutilpy.cvnpy import cvnpath
    import os
    import nibabel as nib

    # calc
    fsdir = os.path.join(cvnpath('freesurfer'),subjectid)

    # input
    if outputdir is None:
      outputdir = os.path.join(fsdir, 'surf')

    if surfsuffix is None:
      surfsuffix = 'orig'

    # prep
    mkdirquiet(outputdir + os.sep)  # note that we add os.sep here

    # load template
    file0 = os.path.join(fsdir, 'surf', '%s.w-g.pct.mgh' % hemi)

    if not os.path.exists(file0):  # fsaverage doesn't have the above file, so let's use this one:
        file0 = os.path.join(fsdir, 'surf','%s.orig.avg.area.mgh' % hemi)

    fsmgh = nib.load(file0)

    # calc
    if surfsuffix == 'orig':
      suffstr = ''
    else:
      suffstr = surfsuffix

    file = os.path.join(outputdir, '%s%s.%s.mgz' % (hemi,suffstr,name))

    ## mangle the field, did this in cvnwritemgz but we will not do here.
    # n = numel(vals);
    # # mangle
    # fsmgh.fspec = file;
    # fsmgh.vol = flatten(vals);
    # fsmgh.volsize = [1 n 1];
    # fsmgh.width = n;
    # fsmgh.nvoxels = n;

    # write
    nib.save(vals.flatten(), file, fsmgh)

