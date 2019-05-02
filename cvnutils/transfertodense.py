def transfertodense(subjectid,vals,hemi,interptype='nearest',surftype='sphere'):
    '''
    def transfertodense(subjectid,vals,hemi,interptype='nearest',surftype='sphere'):

    <subjectid> is like 'C0041'
    <vals> is a column vector of values defined on the regular sphere surface (one hemi)
    <hemi> is 'lh' or 'rh'
    <interptype> is 'linear' or 'nearest', 'cubic'
    <surftype> is 'sphere' (default),'inflated',etc...

    Interpolate to obtain <vals> defined on the dense sphere surface.

    Note that griddata in matlab can only do 'nearest' for 3d interpolation
    griddata in scipy can do 'nearest','linear','cubic' for 3d interpolation

    '''
    from scipy.Interpolate import griddata
    import nibabel.freesurfer.io as fsio

    # calc
    surf1file = cvnpath('freesurfer')/subjectid/'surf'/f'{hemi}.{surftype}'
    surf1file = cvnpath('freesurfer')/subjectid/'surf'/f'{hemi}.{surftype}DENSE'

    # load surfaces (note that we skip the post-processing of vertices and faces since unnecessary for what we are doing)
    surf1.vertices, _ = fsio.read_geometry(surf1file)
    surf2.vertices, _ = fsio.read_geometry(surf2file)

    # do it
    return griddata(surf1.vertices[:,0],surf1.vertices[:,1],surf1.vertices[:,2],vals.flatten(), \
                 surf2.vertices[:,0],surf2.vertices[:,1],surf2.vertices[:,2],method=interptype)