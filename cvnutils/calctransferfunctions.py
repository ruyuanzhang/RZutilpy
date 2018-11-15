def calctransferfunctions(fslhfile, fsrhfile, sslhfile, ssrhfile):

    '''
    cvncalctransferfunctions(fslhfile,fsrhfile,sslhfile,ssrhfile)

    <fslhfile>,<fsrhfile> are locations of the fsaverage spherical surfaces
    <sslhfile>,<ssrhfile> are locations of other surfaces registered on the sphere to fsaverage

    return functions that perform nearest-neigbor interpolation
    to go back and forth between values defined on the surfaces.

    # History
    20180714 now accept pathlib path for all 4 input

    '''

    from nibabel.freesurfer.io import read_geometry
    from scipy.interpolate import griddata
    # load spherical surfaces (note that we skip the post-processing of vertices and faces since unnecessary for what we are doing)
    fslh_vertices, _ = read_geometry(str(fslhfile))
    fsrh_vertices, _ = read_geometry(str(fsrhfile))
    sslh_vertices, _ = read_geometry(str(sslhfile))
    ssrh_vertices, _ = read_geometry(str(ssrhfile))

    # define the functions
    tempix = griddata(fslh_vertices, np.arange(fslh_vertices.shape[0]) + 1, sslh_vertices, method='nearest')
    tfunFSSSlh = lambda x: x[tempix].flatten().astype('float')

    tempix = griddata(fslh_vertices, np.arange(fslh_vertices.shape[0]) + 1, ssrh_vertices, method='nearest')
    tfunFSSSrh = lambda x: x[tempix].flatten().astype('float')

    tempix = griddata(sslh_vertices, np.arange(sslh_vertices.shape[0]) + 1, fslh_vertices, method='nearest')
    tfunSSFSlh = lambda x: x[tempix].flatten().astype('float')

    tempix = griddata(ssrh_vertices, np.arange(ssrh_vertices.shape[0]) + 1, fsrh_vertices, method='nearest')
    tfunSSFSrh = lambda x: x[tempix].flatten().astype('float')

    return tfunFSSSlh,tfunFSSSrh,tfunSSFSlh,tfunSSFSrh
