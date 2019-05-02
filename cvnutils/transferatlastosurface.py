def transferatlastosurface(subjectid, fsmap, hemi, outpre, fstruncate=None,fun=None,outputdir=None):
    '''
    def transferatlastosurface(subjectid, fsmap, hemi, outpre, fstruncate=None,fun=None,outputdir=None):

    <subjectid> is like 'C0001'
    <fsmap> is the fsaverage surface file like '/software/freesurfer/fsaveragemaps/KayDataFFA1-RH.mgz'
    <hemi> is 'lh' or 'rh' indicating whether the surface file is left or right hemisphere
    <outpre> is the prefix of the destination .mgz files to write, like 'KayDataFFA1'
    <fstruncate> is the name of the truncation surface in fsaverage.
     if None, this indicates the non-dense processing case.
    <fun> (optional) is a function to apply to <fsmap> after loading it.
     Default is to do nothing (use values as-is).
    <outputdir> (optional) is the directory to write the .mgz files to.
     Default is cvnpath('freesurfer')/<subjectid>/label/

    Take the <fsmap> file, apply <fun>, and then transfer to single-subject surface space
    using nearest-neighbor interpolation.  Values in the other hemisphere are just set to 0.

    We write three versions:
    (1) <hemi>.<outpre>.mgz - standard (non-dense) surface
    (2) <hemi>DENSE.<outpre>.mgz - dense surface
    (3) <hemi>DENSETRUNC<fstruncate>.<outpre>.mgz - dense, truncated surface

    Note that (2) and (3) are not written if <fstruncate> is [].

    NOTES FROM KEITH:
    cvnroimask looks for label/rh[DENSE|DENSETRUNCpt].roiname.(mgz|mgh|label|annot)
    For multi-label files the label names are contained in a file called
      label/rh[DENSE|DENSETRUNCpt].roiname.(mgz|mgh|label|annot).ctab
    Or possibly without the rh|lh



    # ============== RZ notes ===============================
    Notes:
        * check cvntransferatlastosurface.m
        * <outputdir> now accept both str and a path-like object
        * default <fstruncate>,<fun>,<outputdir> to None

    History:
        20180714 RZ created it based on cvntransferatlastosurface.m
    '''

    from RZutilpy.cvnpy import cvnpath, writemgz
    from RZutilpy.rzio import loadpkl
    from RZutilpy.system import Path, makedirs
    from numpy import zeros

    # internal constants
    fsnumv = 163842  # vertices

    # calc
    fsdir = cvnpath('freesurfer') / subjectid

    # input
    fun = (lambda x: x) if fun is None else fun
    outputdir = fsdir / label if outputdir is None else outputdir
    outputdir = Path(outputdir) if ~isinstance(outputdir, Path) else outputdir

    # load transfer functions
    a1 = loadpkl((cvnpath('anatomicals') / subjectid / 'tfun.pkl').str)

    # load more
    if fstruncate is None:
        a2 = loadpkl((cvnpath('anatomicals')/subjectid/'tfunDENSE.pkl').str)
        # load truncation indices
        a3 = loadpkl((fsdir/'surf'/f'{hemi}.DENSETRUNC{fstruncate}.pkl').str)  # contains 'validix'

    ## !! ## fix here, make sure what load_mgh actually dod
    # load fsaverage map
    vals = flatten(load_mgh(fsmap))  # 1 x 163842
    assert len(vals)==fsnumv
    ## !! ## fix here, make sure what load_mgh actually dod

    # apply fun and expand map into full format (1 x 2*163842)
    vals = hstack((zeros(fsnumv), fun(vals))) if hemi=='rh' else hstack((fun(vals), zeros(1,fsnumv)))

    # make destination directory if necessary
    makedirs(outputdir)

    ##### STANDARD CASE (NON-DENSE)

    # transfer to single subject space (using nearest neighbor interpolation)
    vals0 = a1.tfunFSSSrh(vals) if hemi='rh' else a1.tfunFSSSlh(vals)

    # write mgz
    writemgz(subjectid,outpre,vals0,hemi,outputdir.str)

    ##### DENSE CASES (DENSE ON THE SPHERE ALSO TRUNCATED VERSION)

    if fstruncate is not None:

        # transfer to single subject space (using nearest neighbor interpolation)
        vals0 = a2.tfunFSSSrh(vals) if hemi=='rh' else a2.tfunFSSSlh(vals)

        # write mgz
        writemgz(subjectid,outpre,vals0,hemi+'DENSE',outputdir.str)

        # write mgz (truncated)
        writemgz(subjectid,outpre,vals0[a3.validix], hemi+'DENSETRUNC'+fstruncate, outputdir.str)
