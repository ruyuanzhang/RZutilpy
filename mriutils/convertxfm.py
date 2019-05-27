def convertxfm(xfm, prefix=None):
    '''
    convert an affine transform between lps+ space and ras+ space

    Note that AFNI uses lps+ space, but FSL, Freesurfer, nibabel use ras+ space. This
    function is thus useful to convert and xfm obtained from on space to another


    <xfm>: can be
        (1). ndarray, 12 or 16 elements, can be (12,),(16,)(3,4)(4,4) format
        (2). a string file name, use np.loadtxt to load xfm from the file
    <prefix>: if not None, save the result xfm to the txt file.
    '''
    from numpy import ndarray, hstack, loadtxt, savetxt
    from RZutilpy.system import Path

    if isinstance(xfm, ndarray):
        assert xfm.size==12 or xfm.size==16, 'xfm matrix should be 12 or 16 elements'
    elif isinstance(xfm, str): # read xfm from file
        xfm = loadtxt(xfm)
        assert xfm.size==12 or xfm.size==16, 'xfm matrix should be 12 or 16 elements'

    xfm = xfm.flatten()
    xfm = hstack((xfm, [0,0,0,1])) if xfm.size==12 else xfm

    xfm[[2,3,6,7,8,9]] = -1 * xfm[[2,3,6,7,8,9]]

    xfm = xfm.reshape(4,4)

    if prefix is not None:
        savetxt(Path(prefix).strnosuffix+'.txt', xfm)

    return xfm