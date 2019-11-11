def savevolsmulti(vols, fname, format='nifti'):
    '''
    savevolsmulti(vols, fname, format='nifti'):

    Save a list of vols. We use nibabel

    <vols> a list of ndarrays, vols can have different shape
    <fname> a string pattern for filenames. We input <fname> to rz.rzio.multifilename
        to create a list of filename
    <format>, a str, can be:
        1. 'nifti' (default)
        2. 'mgz', do we need

    Note
        1. do we need to associated .mgz file to each subject??
    '''

    from nibabel import save
